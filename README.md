# FloodWatch AI

Community-powered flood intelligence platform.

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up -d
```

## Tech Stack

- **Backend:** Python/FastAPI
- **Frontend:** Next.js + TypeScript
- **Database:** Supabase PostgreSQL
- **AI:** GPT-5.5 + Whisper
- **Deployment:** Vercel (frontend), Railway (backend)

## Project Structure

```
backend/
├── app/
│   ├── api/v1/        # API endpoints
│   ├── core/          # Config, security, database
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
├── alembic/           # Database migrations
└── tests/             # pytest tests

frontend/
├── app/              # Next.js app router
├── components/       # React components
├── hooks/           # Custom hooks
└── lib/              # Utilities
```

## Documentation

See `/docs/` for detailed documentation:
- ARCHITECTURE_REVIEW.md
- ERD.md
- API_CONTRACTS.md
- SECURITY_REVIEW.md
- DEVELOPMENT_ROADMAP.md