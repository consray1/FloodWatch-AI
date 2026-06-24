# FloodWatch AI - Architecture Review

## 1. System Overview

FloodWatch AI is a community-powered flood intelligence platform that transforms unstructured citizen reports into actionable operational intelligence for disaster response agencies.

**Target Ecosystem:** HUSIKA, ICPAC, disaster response agencies, NGOs

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                         │
├─────────────┬─────────────┬─────────────┬─────────────┬────────────────────┤
│   Web App   │   SMS       │  WhatsApp   │   Voice     │   ICPAC Webhook    │
│  (Next.js)  │  (Twilio)   │  (Twilio)   │  (Whisper)  │   (External)       │
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┴────────┬───────────┘
       │             │             │             │               │
       └─────────────┴─────────────┴─────────────┴───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      API GATEWAY / LOAD       │
                    │         BALANCER              │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │     FASTAPI BACKEND           │
                    │     (Railway/Render)          │
                    │                               │
                    │  ┌─────────────────────────┐ │
                    │  │  Auth Module (JWT)       │ │
                    │  │  Report Module           │ │
                    │  │  Incident Module         │ │
                    │  │  Alert Module            │ │
                    │  │  Analytics Module        │ │
                    │  │  AI Integration          │ │
                    │  │  Webhook Handlers        │ │
                    │  └─────────────────────────┘ │
                    └──────────────┬───────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
           ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│    SUPABASE      │   │   OPENAI API     │   │   EXTERNAL       │
│  ┌────────────┐  │   │  (GPT-5.5 +      │   │   SERVICES       │
│  │ PostgreSQL│  │   │   Whisper)       │   │  ┌────────────┐  │
│  │ Auth      │  │   └──────────────────┘   │  │ Twilio    │  │
│  │ Realtime  │  │                         │  │ Mapbox    │  │
│  └────────────┘  │                         │  │ HUSIKA    │  │
└──────────────────┘                         │  │ ICPAC     │  │
                                              │  └────────────┘  │
                                              └──────────────────┘
```

---

## 3. Component Inventory

### 3.1 Frontend (Next.js + TypeScript)

| Component | Technology | Platform | Purpose |
|-----------|------------|----------|---------|
| Web Application | Next.js 14+ | Vercel | Primary user interface |
| State Management | React Context / Zustand | Client | Application state |
| HTTP Client | Axios / Fetch | Client | API communication |
| Mapping | Leaflet / Mapbox GL | Client | GIS visualization |
| Forms | React Hook Form + Zod | Client | Input validation |

### 3.2 API Server (FastAPI + Python)

| Component | Technology | Platform | Purpose |
|-----------|------------|----------|---------|
| API Framework | FastAPI | Railway/Render | REST API endpoints |
| ORM | SQLAlchemy 2.0 | Local | Database operations |
| Migrations | Alembic | Local | Schema versioning |
| Validation | Pydantic v2 | Local | Request/response validation |
| Auth | Supabase JWT | External | Authentication |
| Task Queue | Celery + Redis | Railway | Background jobs |
| File Storage | Supabase Storage | External | Media files |

### 3.3 Database (Supabase PostgreSQL)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Primary Database | PostgreSQL 15+ | Data storage |
| Auth | Supabase Auth | User authentication |
| Realtime | Supabase Realtime | Live updates |
| Storage | Supabase Storage | File storage |
| Edge Functions | Supabase Edge | Serverless logic |

### 3.4 AI Services

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language Model | GPT-5.5 (OpenAI) | Classification, extraction, summarization |
| Speech-to-Text | Whisper (OpenAI) | Voice report transcription |
| Embeddings | OpenAI Embeddings | Duplicate detection |

### 3.5 External Integrations

| Service | Provider | Purpose |
|---------|----------|---------|
| SMS | Twilio | SMS report submission |
| WhatsApp | Twilio | WhatsApp report submission |
| Voice | Twilio + Whisper | Voice report processing |
| Mapping | Mapbox | GIS visualization |
| Alerts | Twilio / Email | Notification delivery |

---

## 4. Data Flow Diagrams

### 4.1 Report Submission Flow

```
Citizen Submits Report
         │
         ▼
┌─────────────────┐
│  Source Check   │
│  (web/sms/wapp/ │
│   voice/icpac)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Input          │────▶│  Validation     │
│  Normalization  │     │  (Pydantic)     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Media          │     │  Auth           │
│  Processing     │     │  Verification   │
│  (if applicable)│     │  (JWT)          │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Save Report    │
            │  (reports table)│
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Trigger AI     │
            │  Analysis       │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  GPT-5.5        │
            │  Classification │
            │  + Extraction   │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Save Analysis  │
            │  (ai_analysis) │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Duplicate      │
            │  Detection      │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Link to        │
            │  Incident OR    │
            │  Create New     │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Update Trust   │
            │  Score          │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Broadcast      │
            │  Realtime Event │
            └─────────────────┘
```

### 4.2 AI Analysis Flow

```
Report Received
      │
      ▼
┌─────────────────┐
│ Pre-processing  │
│ - Text cleanup  │
│ - Language det. │
└────────┬────────┘
      │
      ▼
┌─────────────────┐
│ GPT-5.5         │
│ Classification  │
│                 │
│ Input: raw_text │
│ Output:         │
│ - hazard_type   │
│ - severity      │
│ - confidence    │
└────────┬────────┘
      │
      ▼
┌─────────────────┐
│ GPT-5.5         │
│ Entity Extract  │
│                 │
│ Extract:        │
│ - locations     │
│ - population    │
│ - infrastructure│
└────────┬────────┘
      │
      ▼
┌─────────────────┐
│ GPT-5.5         │
│ Summarization   │
│                 │
│ Generate:       │
│ - concise brief │
│ - key facts     │
└────────┬────────┘
      │
      ▼
┌─────────────────┐
│ Schema          │
│ Validation      │
│ (Pydantic)      │
└────────┬────────┘
      │
      ▼
┌─────────────────┐
│ Store Results   │
│ Retry on failure│
│ Log all calls   │
└─────────────────┘
```

### 4.3 Incident Creation Flow

```
AI Analysis Complete
        │
        ▼
┌─────────────────┐
│ Check Duplicate │
│ Detection       │
└────────┬────────┘
        │
   ┌────┴────┐
   │ Match?  │
   └────┬────┘
    Yes │ No
   ┌────┴─────────────────┐
   ▼                     ▼
┌────────────┐   ┌────────────────┐
│ Link to    │   │ Create New      │
│ Existing   │   │ Incident        │
│ Incident   │   │                 │
└─────┬──────┘   └────────┬────────┘
      │                   │
      └─────────┬─────────┘
                ▼
      ┌─────────────────┐
      │ Calculate       │
      │ Risk Score      │
      └────────┬────────┘
                │
                ▼
      ┌─────────────────┐
      │ Determine Alert │
      │ Severity        │
      └────────┬────────┘
                │
                ▼
      ┌─────────────────┐
      │ Generate Alert  │
      │ (if needed)     │
      └────────┬────────┘
                │
                ▼
      ┌─────────────────┐
      │ Push Realtime   │
      │ Update          │
      └─────────────────┘
```

### 4.4 Alert Generation Flow

```
Incident Created/Updated
        │
        ▼
┌─────────────────┐
│ Check Alert     │
│ Conditions      │
└────────┬────────┘
        │
   ┌────┴────┐
   │ Threshold│
   │ Met?    │
   └────┬────┘
    Yes │ No
   ┌────┴────────┐
   ▼             ▼
┌────────┐   ┌────────┐
│ Generate│   │ No Alert│
│ Alert  │   │ Action  │
└───┬────┘   └────────┘
    │
    ▼
┌─────────────────┐
│ Select Channels │
│ (sms/email/wapp)│
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Deliver via     │
│ Twilio/SMTP     │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Log Alert       │
│ (audit_logs)    │
└─────────────────┘
```

---

## 5. System Interactions

### 5.1 ICPAC Integration

```
ICPAC External System
        │
        ▼ (Webhook POST /webhooks/icpac)
┌─────────────────┐
│ Verify Source   │
│ IP Allowlist    │
│ HMAC Signature  │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Parse Alert     │
│ Data            │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Transform to    │
│ Internal Format │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Create Incident │
│ (if valid)      │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Trigger         │
│ Internal Alerts │
└─────────────────┘
```

### 5.2 HUSIKA Integration

```
HUSIKA System
        │
        ▼ (API polling or webhook)
┌─────────────────┐
│ Fetch Latest    │
│ Hazard Data     │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Cross-reference │
│ with Existing   │
│ Incidents       │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Update Risk     │
│ Scores          │
└────────┬────────┘
        │
        ▼
┌─────────────────┐
│ Generate        │
│ Recommendations │
└─────────────────┘
```

---

## 6. Technical Decisions

### 6.1 Why FastAPI

| Factor | Decision |
|--------|----------|
| Async Support | Native async/await for I/O-bound operations |
| OpenAPI Auto-gen | Automatic API documentation from type hints |
| Validation | Pydantic v2 provides robust validation |
| Performance | On par with Node.js for REST APIs |
| Ecosystem | Excellent support for ML/AI integration |

### 6.2 Why Supabase

| Factor | Decision |
|--------|----------|
| PostgreSQL | Battle-tested relational database |
| Auth Built-in | Handles JWT + refresh tokens |
| Realtime | Built-in subscriptions for live updates |
| Storage | File storage for media |
| Edge Functions | Serverless logic at the edge |

### 6.3 Why Next.js + Vercel

| Factor | Decision |
|--------|----------|
| SSR | Server-side rendering for SEO |
| API Routes | Backend-for-frontend pattern |
| Edge Functions | Low-latency API responses |
| CDN | Global content delivery |
| Type Safety | Full-stack TypeScript |

### 6.4 Why GPT-5.5 + Whisper

| Factor | Decision |
|--------|----------|
| GPT-5.5 | State-of-the-art language understanding |
| Whisper | Best-in-class speech recognition |
| API-based | No infrastructure management |
| Proven | Extensive track record |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Metric | Target |
|--------|--------|
| API Response Time (p95) | < 500ms |
| Page Load Time | < 2s |
| AI Analysis Latency | < 5s |
| Realtime Update Latency | < 1s |
| Concurrent Users | 1000+ |

### 7.2 Scalability

- Horizontal scaling via container orchestration
- Database connection pooling (PgBouncer)
- CDN for static assets
- Rate limiting per user/IP

### 7.3 Reliability

| Metric | Target |
|--------|--------|
| API Uptime | 99.9% |
| Database Uptime | 99.99% |
| Error Rate | < 0.1% |
| Recovery Time | < 15 min |

### 7.4 Security

| Requirement | Implementation |
|-------------|----------------|
| Encryption at rest | Supabase managed |
| Encryption in transit | TLS 1.3 |
| Authentication | JWT with 15min expiry |
| Password hashing | bcrypt (Supabase) |
| OWASP Top 10 | Full compliance |

---

## 8. Directory Structure

```
floodwatch-ai/
├── frontend/                    # Next.js application
│   ├── app/
│   │   ├── (auth)/             # Auth pages
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/       # Protected pages
│   │   │   ├── reports/
│   │   │   ├── incidents/
│   │   │   ├── alerts/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   ├── api/               # API routes
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/                # Base components
│   │   ├── forms/             # Form components
│   │   ├── maps/              # Map components
│   │   └── dashboard/         # Dashboard widgets
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   ├── auth.ts            # Auth utilities
│   │   └── utils.ts
│   ├── hooks/                 # Custom hooks
│   └── package.json
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth/
│   │   │   │   ├── reports/
│   │   │   │   ├── incidents/
│   │   │   │   ├── alerts/
│   │   │   │   ├── analytics/
│   │   │   │   ├── webhooks/
│   │   │   │   └── system/
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── ai/               # AI integration
│   │   └── main.py
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE_REVIEW.md
│   ├── ERD.md
│   ├── API_CONTRACTS.md
│   ├── SECURITY_REVIEW.md
│   └── DEVELOPMENT_ROADMAP.md
│
├── docker-compose.yml
├── .env.example
├── README.md
└── AGENTS.md
```

---

## 9. Key Architecture Decisions

### 9.1 Report Processing Pipeline

```
Web/SMS/WhatsApp/Voice
         │
         ▼
    API Gateway
         │
         ▼
   Validation Layer
         │
         ▼
   Queue (if async) ───▶ Background Worker
         │                      │
         ▼                      ▼
   Save to DB            AI Analysis
         │                      │
         └──────────┬───────────┘
                    ▼
              Incident Manager
                    │
                    ▼
              Risk Calculator
                    │
                    ▼
              Alert Generator
```

### 9.2 AI Task Routing

| Task | Model | Call Type |
|------|-------|-----------|
| Classification | GPT-5.5 | Synchronous |
| Entity Extraction | GPT-5.5 | Synchronous |
| Summarization | GPT-5.5 | Synchronous |
| Duplicate Detection | Embeddings | Async |
| Voice Transcription | Whisper | Async |

### 9.3 Authentication Flow

```
User Credentials
      │
      ▼
Supabase Auth
      │
      ▼
JWT Access Token (15min) + Refresh Token
      │
      ├──────────────────┐
      ▼                  ▼
Frontend Storage    API Validation
      │                  │
      ▼                  ▼
  Auto-refresh     Verify JWT
  on expiry        with Supabase
```

---

## 10. Future Considerations

### 10.1 Phase 2 Expansions

- Drought monitoring integration
- Landslide detection
- Disease outbreak tracking
- IoT sensor integration

### 10.2 Scaling Triggers

| Metric | Threshold | Action |
|--------|-----------|--------|
| API Latency > 1s | Sustained 5min | Scale backend |
| DB Connections > 80% | Sustained 2min | Add PgBouncer |
| Queue Depth > 1000 | Sustained 10min | Add workers |
| Error Rate > 1% | Sustained 5min | Alert + scale |

---

## 11. External Dependencies

| Service | Purpose | Fallback |
|---------|---------|----------|
| Supabase | Database + Auth | PostgreSQL standalone |
| OpenAI | GPT-5.5 + Whisper | Anthropic Claude |
| Twilio | SMS/WhatsApp/Voice | Other providers |
| Mapbox | Mapping | OpenStreetMap |
| Vercel | Frontend hosting | Netlify |
| Railway | Backend hosting | Render |

---

*Document Version: 1.0*
*Last Updated: 2026-06-24*