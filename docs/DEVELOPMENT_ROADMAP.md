# FloodWatch AI - Development Roadmap

**Version:** 1.0.0
**Last Updated:** 2026-06-24
**Duration:** 12 weeks
**Team Size:** 4-6 developers

---

## 1. Project Phases Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            12-WEEK ROADMAP                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1      Phase 2       Phase 3       Phase 4       Phase 5    Phase 6│
│  Foundation   Core           Advanced      Integration   Frontend  Testing │
│  Week 1-2     Features       Features      Week 7-8     Week 9-10  Week11-12│
│               Week 3-4        Week 5-6                            ║         │
│  ┌──────┐    ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐   ║         │
│  │Setup │    │Reports│      │Duplicate│  │SMS    │      │Dashboard│ ║         │
│  │ DB   │───▶│ AI    │─────▶│Trust   │───▶│WhatsApp│────▶│ Map   │───║──▶ MVP│
│  │Auth  │    │Analysis│    │ Risk   │    │Voice  │      │Forms   │   ║         │
│  └──────┘    └──────┘      └──────┘      └──────┘      └──────┘   ║         │
│                                                             ║         ║         │
│  Milestone M1       M2            M3            M4           M5        M6        │
│  Week 2             Week 4        Week 6        Week 8       Week 10   Week 12 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase Details

### Phase 1: Foundation (Week 1-2)

**Goal:** Set up project infrastructure, database, and API skeleton

#### Week 1: Project Setup

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | Initialize Git repository, add README, AGENTS.md | Repo with basic structure |
| 1-2 | Set up FastAPI project with dependencies | requirements.txt, pyproject.toml |
| 1-2 | Configure Docker + docker-compose.yml | Containerized dev environment |
| 3-4 | Create PostgreSQL schema design | ERD.md finalized |
| 3-4 | Set up Supabase project | Supabase project created |
| 5 | Write Alembic migration | Initial migration file |
| 5-7 | Configure CI/CD pipeline | GitHub Actions workflow |

**Deliverables:**
- [ ] FastAPI project structure
- [ ] Docker Compose with PostgreSQL, Redis
- [ ] Initial database migration
- [ ] CI/CD pipeline
- [ ] .env.example file

#### Week 2: Database & Auth

| Day | Task | Deliverable |
|-----|------|-------------|
| 8-9 | Implement database models (SQLAlchemy) | models/ directory |
| 8-9 | Write Alembic migrations | migrations/versions/ |
| 10-11 | Integrate Supabase Auth | Auth endpoints working |
| 10-11 | Implement JWT token handling | Token utility functions |
| 12-13 | Create user registration/login endpoints | POST /auth/register, /auth/login |
| 14 | Test auth flow end-to-end | Working authentication |

**Deliverables:**
- [ ] All database models
- [ ] Migrations run successfully
- [ ] User registration works
- [ ] JWT tokens generated correctly
- [ ] Supabase Auth integrated

**Milestone M1 (End of Week 2):**
```
✓ FastAPI server running
✓ Database tables created
✓ Authentication working
✓ API returns OpenAPI docs at /docs
```

---

### Phase 2: Core Features (Week 3-4)

**Goal:** Implement report submission and AI analysis

#### Week 3: Report Management

| Day | Task | Deliverable |
|-----|------|-------------|
| 15-16 | Create report CRUD endpoints | POST/GET/PUT/DELETE /reports |
| 15-16 | Implement file upload for media | Report media handling |
| 17-18 | Add report validation | Pydantic schemas |
| 17-18 | Create report filtering/pagination | Query parameters |
| 19-20 | Write report unit tests | tests/test_reports.py |
| 21 | Integrate with Supabase storage | Media URLs in responses |

**Deliverables:**
- [ ] Report CRUD endpoints
- [ ] File upload for images/video/audio
- [ ] Report filtering by status, source, date
- [ ] Pagination implementation
- [ ] Unit tests (>80% coverage)

#### Week 4: AI Integration

| Day | Task | Deliverable |
|-----|------|-------------|
| 22-23 | Set up OpenAI API client | ai/client.py |
| 22-23 | Implement classification prompt | GPT-5.5 classification |
| 24-25 | Implement entity extraction | GPT-5.5 extraction |
| 24-25 | Implement summarization | GPT-5.5 summarization |
| 26-27 | Create AI analysis pipeline | ai/analyzer.py |
| 28 | Add retry/fallback handling | Error handling |

**Deliverables:**
- [ ] OpenAI client configured
- [ ] Classification endpoint (hazard_type, severity, confidence)
- [ ] Entity extraction (locations, population, infrastructure)
- [ ] Summarization generation
- [ ] AI analysis pipeline
- [ ] Retry logic with exponential backoff

**Milestone M2 (End of Week 4):**
```
✓ Reports can be submitted via API
✓ AI analysis runs automatically on new reports
✓ Classification accuracy >80% (verified via tests)
✓ Reports linked to AI analysis results
```

---

### Phase 3: Advanced Features (Week 5-6)

**Goal:** Implement incident management, risk scoring, and alerts

#### Week 5: Incidents & Risk

| Day | Task | Deliverable |
|-----|------|-------------|
| 29-30 | Create incident CRUD endpoints | POST/GET/PUT/DELETE /incidents |
| 29-30 | Implement duplicate detection | Embedding-based similarity |
| 31-32 | Implement incident linking | Link reports to incidents |
| 31-32 | Create trust score system | trust_scores table + logic |
| 33-34 | Implement risk scoring | Risk calculation algorithm |
| 35 | Write incident tests | tests/test_incidents.py |

**Deliverables:**
- [ ] Incident CRUD endpoints
- [ ] Duplicate detection algorithm
- [ ] Automatic incident creation/linking
- [ ] Trust score calculation
- [ ] Risk score algorithm

#### Week 6: Alerts & Real-time

| Day | Task | Deliverable |
|-----|------|-------------|
| 36-37 | Create alert endpoints | POST/GET /alerts |
| 36-37 | Implement alert generation | Auto-alert on high severity |
| 38-39 | Set up Supabase Realtime | WebSocket subscriptions |
| 40-41 | Implement analytics endpoints | GET /analytics/* |
| 40-41 | Add real-time updates to incidents | Pusher/Realtime |
| 42 | Performance optimization | Database query optimization |

**Deliverables:**
- [ ] Alert CRUD endpoints
- [ ] Automatic alert generation
- [ ] Supabase Realtime subscriptions
- [ ] Analytics dashboard data
- [ ] Performance benchmarks met

**Milestone M3 (End of Week 6):**
```
✓ Incidents created from reports
✓ Duplicate reports linked correctly
✓ Risk scores calculated for all incidents
✓ Alerts sent on high-severity incidents
✓ Real-time updates working
```

---

### Phase 4: Integrations (Week 7-8)

**Goal:** Implement webhooks and external integrations

#### Week 7: Webhooks (Inbound)

| Day | Task | Deliverable |
|-----|------|-------------|
| 43-44 | Set up Twilio account | SMS/WhatsApp/Voice configured |
| 43-44 | Implement SMS webhook | POST /webhooks/sms |
| 45-46 | Implement WhatsApp webhook | POST /webhooks/whatsapp |
| 45-46 | Implement voice transcription | POST /webhooks/voice |
| 47-48 | Add Twilio signature verification | Security validation |
| 49 | Test all webhook flows | Integration tests |

**Deliverables:**
- [ ] Twilio integration working
- [ ] SMS reports received and processed
- [ ] WhatsApp reports received and processed
- [ ] Voice recordings transcribed
- [ ] Webhook signature verification

#### Week 8: External Integrations

| Day | Task | Deliverable |
|-----|------|-------------|
| 50-51 | Implement ICPAC webhook | POST /webhooks/icpac |
| 50-51 | Add ICPAC signature verification | HMAC validation |
| 52-53 | Create ICPAC alert transformer | Data format conversion |
| 52-53 | Implement HUSIKA integration | API polling or webhook |
| 54-55 | Set up alert delivery | Twilio SMS/WhatsApp API |
| 56 | Integration testing | End-to-end tests |

**Deliverables:**
- [ ] ICPAC webhook receiver
- [ ] HUSIKA integration
- [ ] Alert delivery via SMS/WhatsApp
- [ ] External system connectivity

**Milestone M4 (End of Week 8):**
```
✓ SMS reports working
✓ WhatsApp reports working
✓ Voice reports working
✓ ICPAC alerts received
✓ External alerts sent
```

---

### Phase 5: Frontend (Week 9-10)

**Goal:** Build the Next.js dashboard

#### Week 9: Core Frontend

| Day | Task | Deliverable |
|-----|------|-------------|
| 57-58 | Initialize Next.js project | Next.js 14+ setup |
| 57-58 | Set up Tailwind CSS + shadcn/ui | UI component library |
| 59-60 | Implement authentication pages | Login/Register |
| 59-60 | Create dashboard layout | Sidebar, header, main |
| 61-62 | Build report submission form | Multi-step form |
| 63-64 | Build reports list view | Table with filters |
| 65 | Write frontend tests | Jest + React Testing Library |

**Deliverables:**
- [ ] Next.js project configured
- [ ] Auth pages (login/register)
- [ ] Dashboard layout
- [ ] Report submission form
- [ ] Reports list view

#### Week 10: Dashboard & Maps

| Day | Task | Deliverable |
|-----|------|-------------|
| 66-67 | Set up Mapbox/Leaflet | Map integration |
| 66-67 | Create incident map view | Interactive map |
| 68-69 | Build incident dashboard | Incident cards/list |
| 68-69 | Build alerts management | Alert list + create |
| 70-71 | Create analytics charts | Recharts/Chart.js |
| 72 | Responsive design | Mobile optimization |

**Deliverables:**
- [ ] Interactive incident map
- [ ] Incident management UI
- [ ] Alert management UI
- [ ] Analytics dashboard
- [ ] Mobile responsive

**Milestone M5 (End of Week 10):**
```
✓ Full dashboard functional
✓ Map showing incidents
✓ Report submission working from web
✓ Alert management UI complete
✓ Analytics charts displaying
```

---

### Phase 6: Testing & Hardening (Week 11-12)

**Goal:** Ensure production-ready quality

#### Week 11: Testing

| Day | Task | Deliverable |
|-----|------|-------------|
| 73-74 | Write API integration tests | tests/api/ |
| 73-74 | Write end-to-end tests | tests/e2e/ |
| 75-76 | Run load testing | k6/load test |
| 75-76 | Fix any test failures | All tests passing |
| 77-78 | Security penetration test | OWASP checklist |
| 79-80 | Performance optimization | Query optimization |

**Deliverables:**
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] 80%+ code coverage
- [ ] Load test results <500ms p95
- [ ] Security vulnerabilities fixed

#### Week 12: Deployment & Documentation

| Day | Task | Deliverable |
|-----|------|-------------|
| 81-82 | Configure Vercel deployment | Frontend on Vercel |
| 81-82 | Configure Railway/Render | Backend on Railway |
| 83-84 | Set up staging environment | staging.floodwatch.ai |
| 83-84 | Configure environment variables | Production .env |
| 85-86 | Write deployment documentation | DEPLOY.md |
| 85-86 | Final code review | All PRs merged |
| 87-88 | Run final tests | Test suite |
| 89 | Demo preparation | Working demo |
| 90 | Hackathon submission | MVP complete |

**Deliverables:**
- [ ] Production deployment
- [ ] Staging environment
- [ ] Deployment documentation
- [ ] All code reviewed
- [ ] Demo working

**Milestone M6 (End of Week 12):**
```
✓ Production deployment complete
✓ All tests passing
✓ 80%+ code coverage
✓ Deployment documentation
✓ MVP ready for demo
```

---

## 3. Milestone Summary

| Milestone | Week | Deliverables | Success Criteria |
|-----------|------|--------------|------------------|
| M1 | 2 | DB + API skeleton | Server runs, docs at /docs |
| M2 | 4 | Reports + AI | AI classification >80% |
| M3 | 6 | Incidents + Alerts | Real-time updates work |
| M4 | 8 | Webhooks | All channels integrated |
| M5 | 10 | Frontend | Full dashboard functional |
| M6 | 12 | MVP Complete | Production-ready |

---

## 4. Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.100+ | API framework |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.11+ | Migrations |
| Pydantic | 2.0+ | Validation |
| Supabase | - | Database + Auth |
| OpenAI | - | GPT-5.5 + Whisper |
| Twilio | - | SMS/WhatsApp/Voice |
| Celery | 5.3+ | Background tasks |
| Redis | 7+ | Task queue backend |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14+ | Framework |
| TypeScript | 5+ | Language |
| Tailwind CSS | 3.4+ | Styling |
| shadcn/ui | - | Components |
| React Query | 5+ | Data fetching |
| Zustand | 4+ | State management |
| Leaflet | 1.9+ | Maps |
| Recharts | 2.10+ | Charts |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Supabase | Database + Auth |
| Vercel | Frontend hosting |
| Railway | Backend hosting |
| GitHub Actions | CI/CD |

---

## 5. Directory Structure

```
floodwatch-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── deps.py          # Dependencies
│   │   │       ├── auth.py          # Auth endpoints
│   │   │       ├── reports.py       # Report endpoints
│   │   │       ├── incidents.py     # Incident endpoints
│   │   │       ├── alerts.py        # Alert endpoints
│   │   │       ├── analytics.py     # Analytics endpoints
│   │   │       ├── webhooks.py      # Webhook endpoints
│   │   │       └── system.py        # Health/metrics
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Settings
│   │   │   ├── security.py          # JWT, passwords
│   │   │   └── database.py         # DB connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── report.py
│   │   │   ├── incident.py
│   │   │   ├── alert.py
│   │   │   └── audit.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── report.py
│   │   │   ├── incident.py
│   │   │   └── alert.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── report.py
│   │   │   ├── incident.py
│   │   │   └── alert.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── client.py            # OpenAI client
│   │   │   └── analyzer.py          # Analysis pipeline
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── session.py
│   │   └── main.py                 # FastAPI app
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_reports.py
│   │   ├── test_incidents.py
│   │   └── test_ai.py
│   ├── .env.example
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx            # Dashboard home
│   │   │   ├── reports/
│   │   │   │   ├── page.tsx        # Reports list
│   │   │   │   └── new/
│   │   │   │       └── page.tsx    # Submit report
│   │   │   ├── incidents/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── alerts/
│   │   │   │   └── page.tsx
│   │   │   └── analytics/
│   │   │       └── page.tsx
│   │   ├── api/
│   │   │   └── [...slug]/
│   │   │       └── route.ts       # API proxy
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                    # shadcn components
│   │   ├── forms/
│   │   │   └── report-form.tsx
│   │   ├── maps/
│   │   │   └── incident-map.tsx
│   │   └── dashboard/
│   │       ├── stats-card.tsx
│   │       └── recent-reports.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── utils.ts
│   ├── hooks/
│   │   ├── use-auth.ts
│   │   └── use-reports.ts
│   ├── types/
│   │   └── index.ts
│   ├── .env.example
│   ├── next.config.js
│   ├── package.json
│   └── tailwind.config.ts
│
├── docs/
│   ├── ARCHITECTURE_REVIEW.md
│   ├── ERD.md
│   ├── API_CONTRACTS.md
│   ├── SECURITY_REVIEW.md
│   └── DEVELOPMENT_ROADMAP.md
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── AGENTS.md
```

---

## 6. Testing Strategy

### Unit Tests (>80% coverage)

```python
# Backend tests structure
tests/
├── conftest.py              # Pytest fixtures
├── test_auth.py             # Authentication tests
├── test_reports.py          # Report CRUD tests
├── test_incidents.py        # Incident tests
├── test_alerts.py           # Alert tests
├── test_ai.py               # AI integration tests
└── test_security.py         # Security tests
```

### Integration Tests

```python
# API integration tests
async def test_report_flow():
    # 1. Create user
    user = await create_test_user()
    # 2. Login
    token = await login_test_user(user)
    # 3. Create report
    report = await create_test_report(token)
    # 4. Verify AI analysis
    analysis = await wait_for_analysis(report.id)
    assert analysis.hazard_type == "flood"
```

### E2E Tests (Playwright)

```typescript
// Frontend e2e tests
describe('Report Submission', () => {
  it('should submit a report successfully', async () => {
    await login('test@example.com', 'password');
    await page.goto('/reports/new');
    await page.fill('textarea[name="raw_text"]', 'Heavy flooding on Mombasa Road');
    await page.click('button[type="submit"]');
    await expect(page.locator('.toast')).toContainText('Report submitted');
  });
});
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      
      - name: Run linting
        run: ruff check backend/
      
      - name: Run type check
        run: mypy backend/
      
      - name: Run tests
        run: pytest backend/tests/ --cov=backend/app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run lint
        run: npm run lint
      
      - name: Run type check
        run: npm run typecheck
      
      - name: Run tests
        run: npm run test
```

---

## 8. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OpenAI API issues | High | Medium | Fallback to cached responses, retry logic |
| Supabase downtime | High | Low | Database backup, connection retry |
| Twilio integration issues | Medium | Medium | Queue messages, manual fallback |
| Performance issues | Medium | Medium | Early load testing, query optimization |
| Security vulnerability | High | Low | Regular audits, OWASP checklist |
| Team availability | High | Medium | Buffer time in schedule |
| Scope creep | Medium | High | Strict MVP scope, defer features |

---

## 9. Communication Plan

| Phase | Sync Frequency | Topics |
|-------|----------------|--------|
| Weekly | Weekly call | Progress, blockers,下周 plan |
| Daily (sprint) | Async standup | Updates, impediments |
| Milestone | Demo day | Show working features |

---

## 10. Definition of Done

Each feature is complete when:

- [ ] Code written and reviewed
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] OpenAPI docs updated
- [ ] No security vulnerabilities
- [ ] Performance acceptable
- [ ] Documentation updated

---

*Document Version: 1.0*
*Last Updated: 2026-06-24*