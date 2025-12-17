from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas
import auth
from database import engine, get_db
from agents.master_agent import run_multi_agent_analysis
from reporting_stub import generate_pdf_report
from utilities import generate_report_id, ensure_reports_dir
import os

# Optional billing imports (for development without Stripe)
try:
    import billing
    import config
    import stripe
    stripe.api_key = config.STRIPE_SECRET_KEY
    BILLING_ENABLED = True
    CORS_ORIGINS = config.CORS_ORIGINS
except ImportError:
    BILLING_ENABLED = False
    print("⚠️  Billing disabled - Stripe not configured. All features available for testing.")
    # Create mock config
    class config:
        FREE_TIER_LIMIT = 999999  # Unlimited for testing
    CORS_ORIGINS = []

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drug Analysis Platform")

# CORS configuration - Specific origins required when using credentials
# IMPORTANT: Must be added BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add exception handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"📝 Signup request received for: {user.username}")
        # Check if user exists
        db_user = db.query(models.User).filter(
            (models.User.email == user.email) | (models.User.username == user.username)
        ).first()
        if db_user:
            print(f"❌ User already exists: {user.username}")
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        hashed_password = auth.get_password_hash(user.password)
        new_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ User created successfully: {user.username}")
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"💥 ERROR in signup: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@app.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    print(f"🔐 Login attempt for user: {user.username}")
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        print(f"❌ Login failed for: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = auth.create_access_token(data={"sub": db_user.username})
    print(f"✅ Token created for: {db_user.username}")
    
    # Set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=86400,  # 24 hours
        path="/",
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    print(f"🍪 Cookie set for: {db_user.username}", flush=True)
    
    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

@app.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/run-analysis")
def run_analysis(
    request: schemas.AnalysisRequest,
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Strategic AI Analysis - Process natural language prompts
    Supports both legacy (drug_name + indication) and new (strategic_prompt) formats
    Authentication is OPTIONAL - works for anonymous users
    """
    from agents.strategic_orchestrator import StrategicOrchestrator
    
    # Check usage limit only if user is authenticated and billing enabled
    if current_user and BILLING_ENABLED and not billing.check_usage_limit(current_user):
        raise HTTPException(
            status_code=403,
            detail=f"Monthly analysis limit reached ({config.FREE_TIER_LIMIT} analyses). Please upgrade to PRO for unlimited access."
        )
    
    # Determine if this is a strategic prompt or legacy format
    if hasattr(request, 'strategic_prompt') and request.strategic_prompt:
        # New strategic prompt format
        orchestrator = StrategicOrchestrator()
        results = orchestrator.process_strategic_prompt(request.strategic_prompt)
        report_id = generate_report_id()
        
        # Increment usage counter (only if user is authenticated and billing enabled)
        if current_user and BILLING_ENABLED:
            billing.increment_usage(current_user, db)
        
        return {
            "report_id": report_id,
            "prompt": request.strategic_prompt,
            "analysis_type": "strategic",
            "results": results
        }
    else:
        # Legacy format: drug_name + indication
        # Convert to strategic prompt format
        prompt = f"Analyze repurposing potential for {request.drug_name} in {request.indication}"
        orchestrator = StrategicOrchestrator()
        results = orchestrator.process_strategic_prompt(prompt)
        report_id = generate_report_id()
        
        # Increment usage counter (only if user is authenticated and billing enabled)
        if current_user and BILLING_ENABLED:
            billing.increment_usage(current_user, db)
        
        return {
            "report_id": report_id,
            "drug_name": request.drug_name,
            "indication": request.indication,
            "analysis_type": "legacy",
            "results": results
        }


@app.post("/generate-strategic-pdf")
def generate_strategic_pdf(
    request: dict,
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    """Generate PDF from strategic analysis results - Available to all users"""
    from agents.strategic_pdf_generator import StrategicPDFGenerator
    from utilities import send_to_n8n
    from config import N8N_WEBHOOK_REPORT_URL
    from datetime import datetime
    import traceback
    
    try:
        print(f"[PDF Generator] Received request: {type(request)}")
        prompt = request.get("prompt", "Strategic Analysis")
        results = request.get("results", {})
        
        print(f"[PDF Generator] Prompt: {prompt}")
        print(f"[PDF Generator] Results keys: {results.keys() if results else 'None'}")
        
        # Generate PDF
        pdf_generator = StrategicPDFGenerator()
        pdf_path = pdf_generator.generate_pdf(prompt, results)
        
        print(f"[PDF Generator] PDF generated at: {pdf_path}")
        
        # Send n8n webhook notification
        print("[PDF Generator] Sending PDF generation webhook to n8n...")
        send_to_n8n(N8N_WEBHOOK_REPORT_URL, {
            "pdf_path": pdf_path,
            "prompt": prompt,
            "user_email": current_user.email if current_user else "anonymous",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })
        
        # Use os.path.basename for Windows compatibility
        filename = os.path.basename(pdf_path)
        
        return {
            "message": "PDF generated successfully",
            "pdf_path": pdf_path,
            "filename": filename
        }
    except Exception as e:
        print(f"[PDF Generator] ERROR: {str(e)}")
        print(f"[PDF Generator] Traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/finalize-report")
def finalize_report(
    request: schemas.ReportFinalize,
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    """Generate final PDF report (Legacy endpoint)"""
    from utilities import send_to_n8n
    from config import N8N_WEBHOOK_REPORT_URL
    from datetime import datetime
    
    # Check if user can generate PDF (only if authenticated user and billing enabled)
    if current_user and BILLING_ENABLED and not billing.can_generate_pdf(current_user):
        raise HTTPException(
            status_code=403,
            detail="PDF generation is a PRO feature. Please upgrade to access this functionality."
        )
    
    ensure_reports_dir()
    
    # Extract drug name and indication from sections
    drug_name = "Drug Analysis"
    indication = "Unknown"
    
    # Try to extract from executive summary or highlights
    if "executive_summary" in request.sections:
        summary = str(request.sections["executive_summary"])
        if "for" in summary:
            parts = summary.split("for")
            if len(parts) > 1:
                drug_indication = parts[1].split("\n")[0].strip()
                if " in " in drug_indication:
                    drug_name, indication = drug_indication.split(" in ", 1)
    
    # Convert sections to simple text format
    text_sections = {}
    for section_name, section_data in request.sections.items():
        if isinstance(section_data, dict):
            text = "\n".join([f"{k}: {v}" for k, v in section_data.items()])
        else:
            text = str(section_data)
        text_sections[section_name] = text
    
    filename = generate_pdf_report(request.report_id, drug_name, text_sections)
    pdf_path = f"reports/report_{request.report_id}.pdf"
    
    # Send n8n webhook notification
    print("[Report Generator] Sending PDF generation webhook to n8n...")
    send_to_n8n(N8N_WEBHOOK_REPORT_URL, {
        "pdf_path": pdf_path,
        "report_id": request.report_id,
        "drug": drug_name,
        "indication": indication,
        "user_email": current_user.email,
        "timestamp": datetime.now().isoformat(),
        "status": "completed"
    })
    
    return {
        "message": "Report generated successfully",
        "report_id": request.report_id,
        "filename": filename
    }

@app.get("/download-report/{filename}")
def download_report(
    filename: str,
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    """Download generated PDF report - Available to all users"""
    # Support both old and new format
    if filename.startswith("report_"):
        filepath = f"reports/{filename}"
    else:
        filepath = f"reports/{filename}"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )

@app.post("/create-checkout-session")
def create_checkout_session(
    request: schemas.CheckoutSessionRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    """Create Stripe checkout session for PRO subscription"""
    if not BILLING_ENABLED:
        raise HTTPException(status_code=501, detail="Billing not configured")
    
    try:
        session = billing.create_checkout_session(
            user_email=current_user.email,
            price_id=request.price_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url
        )
        
        if session:
            return {"sessionId": session.id, "url": session.url}
        else:
            raise HTTPException(status_code=500, detail="Failed to create checkout session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks"""
    if not BILLING_ENABLED:
        raise HTTPException(status_code=501, detail="Billing not configured")
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, config.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        billing.handle_checkout_completed(session, db)
    
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        billing.handle_subscription_updated(subscription, db)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        billing.handle_subscription_deleted(subscription, db)
    
    return {"status": "success"}

@app.get("/subscription-status", response_model=schemas.SubscriptionStatusResponse)
def get_subscription_status(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's subscription status and limits"""
    if not BILLING_ENABLED:
        # Return unlimited access for testing
        return {
            "subscription_tier": "PRO",
            "subscription_status": "active",
            "analyses_this_month": 0,
            "analyses_limit": 999999,
            "can_generate_pdf": True,
            "can_use_rag": True
        }
    
    # Reset monthly counter if needed
    billing.check_usage_limit(current_user)
    db.commit()
    
    analyses_limit = config.PRO_TIER_LIMIT if current_user.subscription_tier == "PRO" else config.FREE_TIER_LIMIT
    
    return {
        "subscription_tier": current_user.subscription_tier,
        "subscription_status": current_user.subscription_status,
        "analyses_this_month": current_user.analyses_this_month,
        "analyses_limit": analyses_limit,
        "can_generate_pdf": billing.can_generate_pdf(current_user),
        "can_use_rag": billing.can_use_rag(current_user)
    }

@app.get("/")
def root():
    return {"message": "Drug Analysis Platform API"}

@app.get("/health")
def health():
    return {"status": "healthy", "cors": "enabled"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
