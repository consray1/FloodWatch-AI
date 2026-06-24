# AGENTS.md

## Repository Overview

**Project:** FloodWatch AI
**Stack:** Python/FastAPI (backend), Next.js + TypeScript (frontend), Supabase (database/auth), OpenAI GPT-5.5 + Whisper (AI)
**Deployment:** Vercel (frontend), Railway/Render (backend), Supabase (DB)

## Key Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head              # Run migrations
uvicorn app.main:app --reload     # Dev server
pytest tests/                     # Tests
ruff check .                      # Lint
mypy app/                         # Type check
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # Dev server
npm run build                     # Production build
npm run lint                      # Lint
npm run typecheck                 # Type check
```

### Infrastructure
```bash
docker-compose up -d             # Local dev services
```

## Architecture Notes

- Backend API at `/api/v1` (FastAPI)
- Supabase handles Auth + PostgreSQL + Realtime
- AI analysis triggered on report creation (GPT-5.5 classification, entity extraction, summarization)
- Webhooks receive reports from SMS (Twilio), WhatsApp (Twilio), Voice (Twilio+Whisper), ICPAC
- Incidents auto-created from reports via duplicate detection (embedding similarity)

## Project Structure

```
/docs/              # Architecture, ERD, API contracts, Security, Roadmap
/backend/app/       # FastAPI application
/frontend/          # Next.js application
```

## Security

- All auth via Supabase (JWT with 15min expiry + refresh tokens)
- RBAC: citizen, responder, analyst, admin
- Webhook endpoints verify signatures (Twilio HMAC, ICPAC HMAC)
- Pydantic validation on all inputs
- RLS enabled on Supabase tables

## Important Files

- `/docs/ARCHITECTURE_REVIEW.md` - Full system design
- `/docs/ERD.md` - Database schema with all tables, relationships, indexes
- `/docs/API_CONTRACTS.md` - OpenAPI 3.0 endpoint specifications
- `/docs/SECURITY_REVIEW.md` - OWASP compliance, threat model, RBAC matrix
- `/docs/DEVELOPMENT_ROADMAP.md` - 12-week implementation plan

## Workflow

1. Plan in `/docs/` first (architecture, specs)
2. Implement backend: models → schemas → services → API endpoints
3. Add AI integration after basic CRUD
4. Build frontend after API stabilized
5. Add webhooks/integrations last

## Testing Requirements

- Backend: pytest with >80% coverage
- Frontend: Jest + React Testing Library
- E2E: Playwright
- Load test with k6 before production