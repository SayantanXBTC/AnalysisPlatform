# Techathon Drug Analysis Platform

Simple AI-powered platform for drug repurposing analysis.

## Quick Start

### Development
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up -d
```

### Deploy to Production
See [DEPLOY_NETLIFY.md](DEPLOY_NETLIFY.md) for complete deployment guide.

**Quick Deploy:**
```bash
# Frontend to Netlify
cd frontend
npm run build
netlify deploy --prod

# Backend to Railway
railway login
railway up
```

## Features
- User authentication
- Strategic drug analysis
- PDF report generation
- Simple and clean interface

## Tech Stack
- Backend: FastAPI + SQLite
- Frontend: React + Vite
- Authentication: JWT cookies
- Reports: ReportLab PDF generation

## Environment Variables
Already configured in `.env` file. No additional setup needed for development.

For production, see [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## Access
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Deployment
- Frontend: Netlify
- Backend: Railway or Render
- Database: PostgreSQL (auto-provisioned)

See [DEPLOY_NETLIFY.md](DEPLOY_NETLIFY.md) for step-by-step instructions.