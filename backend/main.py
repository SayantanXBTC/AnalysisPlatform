from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models
import schemas
import auth
from database import engine, get_db
from agents.strategic_orchestrator import StrategicOrchestrator
from utilities import generate_report_id
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drug Analysis Platform")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if db_user:
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
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": db_user.username})
    
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
def run_analysis(request: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    """Strategic AI Analysis - Process natural language prompts"""
    orchestrator = StrategicOrchestrator()
    
    # Handle both strategic prompt and legacy format
    if hasattr(request, 'strategic_prompt') and request.strategic_prompt:
        results = orchestrator.process_strategic_prompt(request.strategic_prompt)
        prompt = request.strategic_prompt
    else:
        # Legacy format: drug_name + indication
        prompt = f"Analyze repurposing potential for {request.drug_name} in {request.indication}"
        results = orchestrator.process_strategic_prompt(prompt)
    
    report_id = generate_report_id()
    
    return {
        "report_id": report_id,
        "prompt": prompt,
        "results": results
    }


@app.post("/generate-strategic-pdf")
def generate_strategic_pdf(request: dict):
    """Generate PDF from strategic analysis results"""
    from agents.strategic_pdf_generator import StrategicPDFGenerator
    
    prompt = request.get("prompt", "Strategic Analysis")
    results = request.get("results", {})
    
    # Generate PDF
    pdf_generator = StrategicPDFGenerator()
    pdf_path = pdf_generator.generate_pdf(prompt, results)
    
    filename = os.path.basename(pdf_path)
    
    return {
        "message": "PDF generated successfully",
        "pdf_path": pdf_path,
        "filename": filename
    }

@app.get("/download-report/{filename}")
def download_report(filename: str):
    """Download generated PDF report"""
    filepath = f"reports/{filename}"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )

@app.get("/")
def root():
    return {"message": "Drug Analysis Platform API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
