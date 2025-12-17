import os
from dotenv import load_dotenv

load_dotenv()

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID_PRO = os.getenv("STRIPE_PRICE_ID_PRO", "price_1234567890")

# App Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# CORS Origins
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Subscription Limits
FREE_TIER_LIMIT = 5  # analyses per month
PRO_TIER_LIMIT = 999999  # unlimited

# n8n Webhook Configuration
N8N_WEBHOOK_REPORT_URL = os.getenv("N8N_WEBHOOK_REPORT_URL", "https://your-n8n-url/webhook/report-created")
N8N_WEBHOOK_ANALYSIS_URL = os.getenv("N8N_WEBHOOK_ANALYSIS_URL", "https://your-n8n-url/webhook/analysis-finished")
N8N_IQVIA_URL = os.getenv("N8N_IQVIA_URL", "https://your-n8n-url/webhook/iqvia_mock")
N8N_EXIM_URL = os.getenv("N8N_EXIM_URL", "https://your-n8n-url/webhook/exim_mock")
