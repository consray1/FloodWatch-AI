# FloodWatch AI - Security Review

**Version:** 1.0.0
**Last Updated:** 2026-06-24

---

## 1. Security Model Overview

FloodWatch AI follows **Secure by Design** principles with defense in depth.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SECURITY LAYERS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Layer 1: Network Security                                                 │
│  ├── HTTPS everywhere (TLS 1.3)                                           │
│  ├── API Gateway (rate limiting, WAF)                                     │
│  └── VPC/private networking                                                │
│                                                                             │
│  Layer 2: Authentication & Authorization                                  │
│  ├── JWT with short expiry (15 min)                                       │
│  ├── Refresh token rotation                                               │
│  ├── RBAC with 4 roles                                                     │
│  └── Supabase Auth integration                                             │
│                                                                             │
│  Layer 3: Input Validation & Sanitization                                 │
│  ├── Pydantic v2 validation                                               │
│  ├── Output encoding                                                       │
│  └── SQL injection prevention (ORM)                                        │
│                                                                             │
│  Layer 4: Data Protection                                                   │
│  ├── Encryption at rest (Supabase managed)                                 │
│  ├── Encryption in transit                                                 │
│  ├── PII handling procedures                                               │
│  └── Audit logging                                                         │
│                                                                             │
│  Layer 5: Monitoring & Response                                            │
│  ├── Real-time anomaly detection                                          │
│  ├── Automated alerting                                                    │
│  └── Incident response plan                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Threat Model

### 2.1 Assets to Protect

| Asset | Value | Threats |
|-------|-------|---------|
| User credentials | Critical | Theft, brute force |
| Personal data (PII) | High | Exposure, theft |
| Report data | High | Manipulation, deletion |
| Incident data | High | Manipulation, spoofing |
| API availability | High | DoS, DDoS |
| AI model integrity | Medium | Manipulation |

### 2.2 Threat Actors

| Actor | Capability | Intent |
|-------|------------|--------|
| Anonymous user | Basic | Reconnaissance |
| Malicious user | Registered account | Data manipulation |
| Insider (low) | Employee access | Data exfiltration |
| Insider (high) | Admin access | System compromise |
| Script kiddie | Automated tools | DoS, vandalism |
| Organized | Advanced APT | Data theft, disruption |

### 2.3 Attack Vectors

```
                    INTERNET
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   API GATEWAY                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   │
│  │ Rate Limit│  │    WAF    │  │ IP Allowlist     │   │
│  │ 100/min   │  │ OWASP CRS │  │ (webhooks only)  │   │
│  └───────────┘  └───────────┘  └───────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   │
│  │ JWT Auth │  │ RBAC      │  │ Input Validation  │   │
│  │ 15min    │  │ 4 roles   │  │ Pydantic v2      │   │
│  └───────────┘  └───────────┘  └───────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Supabase │  │ OpenAI   │  │ External │
    │ Database │  │ API      │  │ Services │
    └──────────┘  └──────────┘  └──────────┘
```

### 2.4 Data Flow Threat Analysis

```
User Input → API Gateway → Validation → Auth Check → RBAC → DB → Response
     │           │            │           │          │      │
     ▼           ▼            ▼           ▼          ▼      ▼
  Injection   DoS          Bypass      Token      PrivEsc  Breach
  XSS         Brute        Tamper      Theft       Abuse    Exposure
```

---

## 3. OWASP Top 10 Compliance

### A01: Broken Access Control

**Risk:** Unauthorized access to resources

**Mitigations:**
```python
# 1. Role-based access control
ROLES = {
    "citizen": ["read:own_reports", "create:reports", "read:incidents"],
    "responder": ["read:all", "create:incidents", "update:incidents", "create:alerts"],
    "analyst": ["read:analytics", "read:all_reports"],
    "admin": ["*"]  # Full access
}

# 2. Resource ownership checks
async def check_report_access(user_id: uuid, report_id: uuid) -> bool:
    report = await db.get_report(report_id)
    if report.reporter_id == user_id:
        return True
    if user.role in ["responder", "analyst", "admin"]:
        return True
    return False

# 3. Row-level security (Supabase RLS)
CREATE POLICY "reports_owner_access" ON reports
    FOR ALL USING (auth.uid() = reporter_id OR
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid()
            AND role_id IN (responder_role, analyst_role, admin_role)));
```

**Validation:**
```python
# Test cases
assert check_access(citizen, own_report) == True
assert check_access(citizen, other_report) == False
assert check_access(responder, any_report) == True
assert check_access(responder, create_incident) == True
assert check_access(citizen, create_incident) == False
```

---

### A02: Cryptographic Failures

**Risk:** Data exposure through weak cryptography

**Mitigations:**
```python
# 1. Password hashing (Supabase uses bcrypt)
# Minimum requirements enforced by Supabase:
# - Minimum 8 characters
# - No common passwords
# - Email not used as password

# 2. JWT security
JWT_CONFIG = {
    "algorithm": "HS256",
    "access_token_expiry": 900,  # 15 minutes
    "refresh_token_expiry": 604800,  # 7 days
    "refresh_token_rotation": True  # Each use generates new refresh token
}

# 3. Secure secret management
# NEVER hardcode secrets - use environment variables
# Railway/Render: Config Vars
# Local: .env file (gitignored)
SECRET_KEY = os.getenv("SECRET_KEY")  # Minimum 32 chars

# 4. TLS configuration
# All external connections require TLS 1.3
# Supabase: Enforced TLS
# OpenAI: TLS 1.2+
# Twilio: TLS required
```

---

### A03: Injection

**Risk:** SQL, NoSQL, Command injection

**Mitigations:**
```python
# 1. SQLAlchemy ORM prevents SQL injection
# All queries use parameterized statements
result = await db.execute(
    select(Report).where(Report.id == report_id)
)

# 2. Pydantic input validation
class ReportCreate(BaseModel):
    raw_text: constr(min_length=10, max_length=5000)
    location_lat: Optional[float] = Field(ge=-90, le=90)
    location_lng: Optional[float] = Field(ge=-180, le=180)

# 3. Output encoding
from fastapi.responses import JSONResponse
# All outputs JSON-serialized by FastAPI

# 4. Whitelist validation for webhooks
VALID_IPS = [
    "54.172.0.0/15",  # Twilio
    "10.0.0.0/8"      # ICPAC internal
]

def verify_source_ip(ip: str) -> bool:
    return any(ip in cidr for cidr in VALID_IPS)
```

---

### A04: Insecure Design

**Risk:** Architectural weaknesses

**Mitigations:**
```python
# 1. Threat modeling during design phase
THREAT_MODEL = {
    "report_submission": {
        "threats": ["spam", "malicious_content", "data_manipulation"],
        "mitigations": ["rate_limit", "content_filter", "ai_analysis"]
    },
    "authentication": {
        "threats": ["brute_force", "credential_stuffing", "session_hijacking"],
        "mitigations": ["rate_limit", "mfa", "refresh_token_rotation"]
    },
    "webhooks": {
        "threats": ["spoofing", "replay", " tampering"],
        "mitigations": ["signature_verify", "timestamp_check", "https"]
    }
}

# 2. Secure defaults
# All endpoints require auth except:
# - POST /auth/login
# - POST /auth/register
# - GET /health
# - POST /webhooks/* (signature verified)

# 3. Fail securely
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

### A05: Security Misconfiguration

**Risk:** Improperly configured security controls

**Mitigations:**
```python
# 1. CORS configuration
CORS_CONFIG = {
    "allow_origins": ["https://floodwatch.vercel.app"],
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type"],
    "allow_credentials": True,
    "max_age": 600
}

# 2. Security headers
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# 3. Environment-based configuration
class Settings(BaseSettings):
    DEBUG: bool = False  # Never True in production
    API_VERSION: str = "1.0.0"
    CORS_ORIGINS: list[str] = ["https://floodwatch.vercel.app"]

# 4. Database security
# - No default passwords
# - Limited user privileges
# - Connection pooling with PgBouncer
# - Row-level security enabled
```

---

### A06: Vulnerable Components

**Risk:** Outdated or vulnerable dependencies

**Mitigations:**
```bash
# 1. Regular dependency updates
pip install --upgrade -r requirements.txt

# 2. Automated scanning
# requirements.txt pinned versions
# Dependabot alerts enabled

# 3. Python-specific checks
safety check
pip-audit

# 4. Frontend dependencies
npm audit
Snyk or Dependabot for JavaScript
```

**Critical Dependencies:**
| Package | Min Version | Reason |
|---------|-------------|--------|
| FastAPI | 0.100+ | Security patches |
| Pydantic | 2.0+ | Validation security |
| SQLAlchemy | 2.0+ | Query parameterization |
| python-jose | 3.3+ | JWT security |
| passlib | 1.7+ | Password hashing |

---

### A07: Identification and Authentication Failures

**Risk:** Account compromise

**Mitigations:**
```python
# 1. Supabase Auth (built-in protections)
# - Brute force protection
# - Account lockout after 5 failed attempts
# - Password strength requirements
# - Email verification required

# 2. JWT security
ACCESS_TOKEN_EXPIRY = 900  # 15 minutes
REFRESH_TOKEN_EXPIRY = 604800  # 7 days
REFRESH_TOKEN_ROTATION = True

# 3. Session management
SESSION_CONFIG = {
    "max_sessions_per_user": 5,
    "session_timeout": 3600,  # 1 hour of inactivity
    "absolute_timeout": 86400  # 24 hours max
}

# 4. Audit logging
AUTH_LOG_EVENTS = [
    "login_success",
    "login_failed",
    "logout",
    "password_reset_request",
    "password_reset_complete",
    "session_expired"
]
```

---

### A08: Software and Data Integrity Failures

**Risk:** Tampering with code or data

**Mitigations:**
```yaml
# 1. CI/CD pipeline security
# - Code signing required
# - No direct production pushes
# - Deployment approval required
# - Immutable artifacts

# 2. Dependency verification
# - Lockfiles required
# - Hash verification
# - Private package registry

# 3. Database migrations
# - All migrations versioned
# - Rollback capability
# - No direct prod DB access
```

---

### A09: Security Logging and Monitoring

**Risk:** Undetected attacks

**Mitigations:**
```python
# 1. Comprehensive logging
LOG_EVENTS = [
    # Authentication
    ("login", "INFO"),
    ("login_failed", "WARN"),
    ("logout", "INFO"),
    ("token_refresh", "DEBUG"),
    
    # Authorization
    ("access_denied", "WARN"),
    ("privilege_escalation_attempt", "CRITICAL"),
    
    # Data operations
    ("report_create", "INFO"),
    ("report_delete", "WARN"),
    ("incident_modify", "INFO"),
    
    # Security events
    ("rate_limit_exceeded", "WARN"),
    ("invalid_signature", "WARN"),
    ("suspicious_activity", "CRITICAL")
]

# 2. Log structure
LOG_FORMAT = {
    "timestamp": "ISO8601",
    "level": "INFO/WARN/ERROR",
    "event": "event_name",
    "actor_id": "uuid",
    "actor_ip": "ip_address",
    "resource": "resource_type/id",
    "action": "action_taken",
    "status": "success/failure",
    "details": {}
}

# 3. Monitoring
# - Prometheus metrics
# - Error rate alerting
# - Latency spike detection
# - Unusual activity patterns
```

---

### A10: Server-Side Request Forgery (SSRF)

**Risk:** Internal service compromise

**Mitigations:**
```python
# 1. URL validation for webhooks
from urllib.parse import urlparse

ALLOWED_HOSTS = [
    "api.twilio.com",
    "functions.supabase.co",
    "api.openai.com"
]

def validate_webhook_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False
    if parsed.hostname not in ALLOWED_HOSTS:
        return False
    return True

# 2. IP allowlisting for webhooks
ICPAC_IPS = ["10.0.0.0/8"]  # Internal network
TWILIO_IPS = ["54.172.0.0/15"]

# 3. No user-provided URLs for external requests
# All external API calls use predefined endpoints
```

---

## 4. RBAC Matrix

### 4.1 Role Definitions

| Role | Description | Default |
|------|-------------|---------|
| citizen | Community reporter | Yes |
| responder | Emergency responder | No |
| analyst | ICPAC analyst | No |
| admin | System administrator | No |

### 4.2 Permission Matrix

| Resource | Action | citizen | responder | analyst | admin |
|----------|--------|---------|-----------|---------|-------|
| **Reports** | | | | | |
| | create | ✓ | ✓ | ✓ | ✓ |
| | read (own) | ✓ | ✓ | ✓ | ✓ |
| | read (all) | - | ✓ | ✓ | ✓ |
| | update (own) | ✓ | ✓ | ✓ | ✓ |
| | delete (own) | ✓ | ✓ | ✓ | ✓ |
| **Incidents** | | | | | |
| | create | - | ✓ | - | ✓ |
| | read | ✓ | ✓ | ✓ | ✓ |
| | update | - | ✓ | - | ✓ |
| | delete | - | - | - | ✓ |
| **Alerts** | | | | | |
| | create | - | ✓ | - | ✓ |
| | read | - | ✓ | ✓ | ✓ |
| | update | - | ✓ | - | ✓ |
| | delete | - | - | - | ✓ |
| **Analytics** | | | | | |
| | read (basic) | ✓ | ✓ | ✓ | ✓ |
| | read (full) | - | - | ✓ | ✓ |
| **Users** | | | | | |
| | create | - | - | - | ✓ |
| | read (all) | - | - | - | ✓ |
| | update roles | - | - | - | ✓ |
| | deactivate | - | - | - | ✓ |

---

## 5. Input Validation

### 5.1 Pydantic Schemas

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ReportCreate(BaseModel):
    source: Literal["web", "sms", "whatsapp", "voice", "icpac"]
    raw_text: str = Field(..., min_length=10, max_length=5000)
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=255)

    @validator("raw_text")
    def sanitize_text(cls, v):
        # Remove control characters
        v = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", v)
        return v.strip()

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, regex=r"^\+[1-9]\d{1,14}$")
    password: str = Field(..., min_length=8)

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain digit")
        return v
```

---

## 6. Rate Limiting

### 6.1 Limits by Endpoint

| Endpoint | Limit | Window | Response |
|----------|-------|--------|----------|
| POST /auth/login | 10 | 1 min | 429 |
| POST /auth/register | 5 | 1 min | 429 |
| POST /reports | 20 | 1 min | 429 |
| GET /reports | 100 | 1 min | 429 |
| POST /incidents | 10 | 1 min | 429 |
| POST /alerts | 10 | 1 min | 429 |
| Webhooks | 1000 | 1 min | 200 |

### 6.2 Implementation

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/reports")
@limiter.limit("20/minute")
async def create_report(request: Request, data: ReportCreate):
    # Handle report
    pass

# Redis-backed rate limiting for production
REDIS_URL = os.getenv("REDIS_URL")
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL
)
```

---

## 7. Encryption

### 7.1 Data at Rest

| Data Type | Encryption | Method |
|-----------|------------|--------|
| Database | Supabase managed | AES-256 |
| File Storage | Supabase managed | AES-256 |
| Backups | Supabase managed | AES-256 |

### 7.2 Data in Transit

| Connection | Protocol | Version |
|------------|----------|---------|
| Client → API | HTTPS | TLS 1.3 |
| API → Database | Internal | TLS 1.3 |
| API → OpenAI | HTTPS | TLS 1.2+ |
| API → Twilio | HTTPS | TLS 1.2+ |

---

## 8. Audit Logging

### 8.1 Logged Events

```python
AUDIT_EVENTS = {
    # Authentication
    "auth.login": {"level": "INFO", "PII": False},
    "auth.login_failed": {"level": "WARN", "PII": False},
    "auth.logout": {"level": "INFO", "PII": False},
    "auth.register": {"level": "INFO", "PII": True},  # contains email
    "auth.token_refresh": {"level": "DEBUG", "PII": False},

    # Data access
    "report.create": {"level": "INFO", "PII": True},  # contains text
    "report.read": {"level": "DEBUG", "PII": True},
    "report.update": {"level": "INFO", "PII": True},
    "report.delete": {"level": "WARN", "PII": True},
    "incident.create": {"level": "INFO", "PII": False},
    "incident.update": {"level": "INFO", "PII": False},
    "incident.delete": {"level": "WARN", "PII": False},

    # Security
    "security.rate_limited": {"level": "WARN", "PII": False},
    "security.invalid_signature": {"level": "WARN", "PII": False},
    "security.access_denied": {"level": "WARN", "PII": False},
    "security.privilege_escalation": {"level": "CRITICAL", "PII": False},

    # Admin
    "admin.user_role_change": {"level": "WARN", "PII": True},
    "admin.user_deactivate": {"level": "WARN", "PII": True},
    "admin.config_change": {"level": "CRITICAL", "PII": False}
}
```

### 8.2 Log Retention

| Log Type | Retention | Storage |
|----------|-----------|---------|
| Auth logs | 1 year | Supabase |
| Audit logs | 1 year | Supabase |
| Security logs | 1 year | Supabase |
| Error logs | 90 days | Railway logs |

---

## 9. Security Checklist

### Pre-Development
- [ ] Threat model completed
- [ ] Security requirements reviewed
- [ ] OWASP Top 10 checklist reviewed
- [ ] Secure coding standards documented

### During Development
- [ ] All user input validated
- [ ] All database queries use ORM
- [ ] No secrets in code
- [ ] PII handling documented
- [ ] RBAC implemented correctly

### Pre-Deployment
- [ ] Security scan completed
- [ ] Dependency audit passed
- [ ] Penetration test (if possible)
- [ ] Rate limiting configured
- [ ] Logging enabled

### Post-Deployment
- [ ] Monitoring active
- [ ] Alerts configured
- [ ] Backup tested
- [ ] Incident response plan ready

---

## 10. Incident Response

### 10.1 Severity Levels

| Level | Definition | Response Time |
|-------|------------|---------------|
| P1 | Active breach, data exposure | 15 minutes |
| P2 | Suspected breach, major vulnerability | 1 hour |
| P3 | Security misconfiguration | 24 hours |
| P4 | Minor vulnerability | 1 week |

### 10.2 Response Steps

```
1. Identify - Determine scope and severity
2. Contain - Isolate affected systems
3. Eradicate - Remove threat
4. Recover - Restore normal operations
5. Post-mortem - Document lessons learned
```

### 10.3 Contact Information

| Role | Contact |
|------|---------|
| Security Team | security@floodwatch.ai |
| On-call | oncall@floodwatch.ai |
| Emergency | emergency@floodwatch.ai |

---

*Document Version: 1.0*
*Last Updated: 2026-06-24*