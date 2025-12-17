from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    subscription_tier: str = "FREE"
    subscription_status: str = "inactive"
    analyses_this_month: int = 0
    
    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    # Support both legacy and new strategic prompt formats
    drug_name: Optional[str] = None
    indication: Optional[str] = None
    strategic_prompt: Optional[str] = None
    
    class Config:
        # Allow either strategic_prompt OR (drug_name + indication)
        pass

class ReportFinalize(BaseModel):
    report_id: str
    sections: dict

class CheckoutSessionRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str

class SubscriptionStatusResponse(BaseModel):
    subscription_tier: str
    subscription_status: str
    analyses_this_month: int
    analyses_limit: int
    can_generate_pdf: bool
    can_use_rag: bool