# FloodWatch AI - Entity Relationship Diagram

## Database: PostgreSQL 15+ (Supabase)

---

## 1. Entity Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USERS & AUTH                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐         ┌──────────┐         ┌──────────────────────────┐   │
│   │  roles   │         │  users   │         │     trust_scores        │   │
│   ├──────────┤         ├──────────┤         ├──────────────────────────┤   │
│   │ id (PK)  │◄──────┐ │ id (PK)  │         │ id (PK)                 │   │
│   │ name     │       │ │ name     │         │ user_id (FK) ──────────┼─┼ │
│   └──────────┘       │ │ email    │         │ score (0-100)           │   │
│         │            │ │ phone    │         │ created_at              │   │
│         │            │ │ role_id  │─────────┤ updated_at              │   │
│         │            │ │ created  │         └──────────────────────────┘   │
│         │            │ │ _at      │                                           │
│         │            │ └──────────┘                                           │
│         │            │       │                                                │
│         │            │       │ 1:N                                           │
│         │            │       ▼                                                │
│         │            │ ┌──────────┐                                          │
│         └────────────│─│ reports  │                                          │
│                      │ ├──────────┤                                          │
│                      │ │ id (PK)  │                                          │
│                      │ │ source   │                                          │
│                      │ │ raw_text │                                          │
│                      │ │ reporter │                                         │
│                      │ │ _id(FK)  │                                         │
│                      │ │ created  │                                         │
│                      │ └──────────┘                                          │
│                              │                                               │
│                              │ 1:1                                          │
│                              ▼                                               │
│                      ┌──────────────┐                                       │
│                      │  ai_analysis │                                       │
│                      ├──────────────┤                                       │
│                      │ id (PK)      │                                       │
│                      │ report_id(FK)│                                       │
│                      │ hazard_type  │                                       │
│                      │ severity     │                                       │
│                      │ confidence   │                                       │
│                      │ summary       │                                       │
│                      └──────────────┘                                       │
│                              │                                               │
│                              │ N:M (via incident_reports)                   │
│                              ▼                                               │
│                      ┌──────────────┐      ┌────────────────────┐          │
│                      │  incidents   │◄─────│ incident_reports   │          │
│                      ├──────────────┤      ├────────────────────┤          │
│                      │ id (PK)      │      │ incident_id (FK)   │          │
│                      │ title        │      │ report_id (FK)     │          │
│                      │ description  │      └────────────────────┘          │
│                      │ severity     │                                        │
│                      │ latitude     │                                        │
│                      │ longitude    │                                        │
│                      │ status       │                                        │
│                      │ created_at   │                                        │
│                      └──────────────┘                                        │
│                              │                                               │
│                              │ 1:N                                           │
│                              ▼                                               │
│                      ┌──────────────┐                                       │
│                      │  risk_scores │                                       │
│                      ├──────────────┤                                       │
│                      │ id (PK)      │                                       │
│                      │ incident_id  │                                       │
│                      │ score        │                                       │
│                      │ created_at   │                                       │
│                      └──────────────┘                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              ALERTS & NOTIFICATIONS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐         ┌──────────┐                                        │
│   │  alerts  │         │ audit_   │                                        │
│   ├──────────┤         │ logs     │                                        │
│   │ id (PK)  │         ├──────────┤                                        │
│   │ title    │         │ id (PK)  │                                        │
│   │ message  │         │ actor_id │                                        │
│   │ severity │         │ action   │                                        │
│   │ channel  │         │ entity   │                                        │
│   │ sent_at  │         │ details  │                                        │
│   └──────────┘         │ created  │                                        │
│                        │ _at      │                                        │
│                        └──────────┘                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              REPORT MEDIA                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐         ┌────────────────┐                             │
│   │   reports    │  1:N    │  report_media  │                             │
│   ├──────────────┤─────────│ ──────────────  │                             │
│   │ id (PK)      │         │ id (PK)        │                             │
│   │ source       │         │ report_id (FK) │                             │
│   │ raw_text     │         │ media_url      │                             │
│   │ reporter_id  │         │ media_type     │                             │
│   │ created_at   │         │ created_at     │                             │
│   └──────────────┘         └────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              INFRASTRUCTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐         ┌──────────┐         ┌──────────┐                 │
│   │ shelters │         │hospitals │         │  roles   │                 │
│   ├──────────┤         ├──────────┤         ├──────────┤                 │
│   │ id (PK)  │         │ id (PK)  │         │ id (PK)  │                 │
│   │ name     │         │ name     │         │ name     │                 │
│   │ latitude │         │ latitude │         └──────────┘                 │
│   │ longitude│         │ longitude│              │                       │
│   │ capacity │         │ phone    │              │                       │
│   │ occupancy│         └──────────┘              │                       │
│   └──────────┘                                    │                       │
│                                                     │                       │
│                                                     ▼                       │
│                                              ┌──────────┐                 │
│                                              │  users   │                 │
│                                              ├──────────┤                 │
│                                              │ id (PK)  │                 │
│                                              │ role_id  │───────────────┘
│                                              └──────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Table Definitions

### 2.1 Core Tables

#### `roles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Role name |
| description | TEXT | | Role description |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:** `idx_roles_name` ON `name`

**Roles Seed Data:**
```sql
('citizen', 'Community member who can submit reports'),
('responder', 'Emergency responder who can manage incidents'),
('analyst', 'AI/ICPAC analyst who can view analytics'),
('admin', 'System administrator with full access');
```

---

#### `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| phone | VARCHAR(20) | UNIQUE | Phone number |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| role_id | UUID | FK → roles.id, DEFAULT 'citizen' | User role |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verified |
| last_login | TIMESTAMP | | Last login time |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_users_email` ON `email`
- `idx_users_phone` ON `phone`
- `idx_users_role_id` ON `role_id`

**Constraints:**
```sql
ALTER TABLE users ADD CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$');
ALTER TABLE users ADD CONSTRAINT chk_phone_format CHECK (phone ~* '^\+[1-9]{1}[0-9]{1,14}$');
```

---

#### `reports`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| source | VARCHAR(20) | NOT NULL | web, sms, whatsapp, voice, icpac |
| reporter_id | UUID | FK → users.id, NULLABLE | Reporter (NULL for anonymous) |
| raw_text | TEXT | NOT NULL | Original report text |
| location_lat | DECIMAL(10,8) | | Latitude |
| location_lng | DECIMAL(11,8) | | Longitude |
| location_name | VARCHAR(255) | | Location description |
| status | VARCHAR(20) | DEFAULT 'pending' | pending, analyzed, verified, dismissed |
| language | VARCHAR(10) | DEFAULT 'en' | Report language |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_reports_reporter_id` ON `reporter_id`
- `idx_reports_status` ON `status`
- `idx_reports_source` ON `source`
- `idx_reports_created_at` ON `created_at DESC`
- `idx_reports_location` ON `location_lat, location_lng`

**Constraints:**
```sql
ALTER TABLE reports ADD CONSTRAINT chk_source CHECK (source IN ('web', 'sms', 'whatsapp', 'voice', 'icpac'));
ALTER TABLE reports ADD CONSTRAINT chk_status CHECK (status IN ('pending', 'analyzed', 'verified', 'dismissed'));
ALTER TABLE reports ADD CONSTRAINT chk_location_lat CHECK (location_lat >= -90 AND location_lat <= 90);
ALTER TABLE reports ADD CONSTRAINT chk_location_lng CHECK (location_lng >= -180 AND location_lng <= 180);
```

---

#### `report_media`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| report_id | UUID | FK → reports.id, NOT NULL | Parent report |
| media_url | VARCHAR(500) | NOT NULL | Media file URL |
| media_type | VARCHAR(20) | NOT NULL | image, video, audio |
| file_size | INTEGER | | File size in bytes |
| mime_type | VARCHAR(50) | | MIME type |
| created_at | TIMESTAMP | DEFAULT NOW() | Upload timestamp |

**Indexes:**
- `idx_report_media_report_id` ON `report_id`

**Constraints:**
```sql
ALTER TABLE report_media ADD CONSTRAINT chk_media_type CHECK (media_type IN ('image', 'video', 'audio'));
```

---

#### `ai_analysis`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| report_id | UUID | FK → reports.id, UNIQUE, NOT NULL | Parent report |
| hazard_type | VARCHAR(50) | | flood, landslide, storm, etc. |
| hazard_category | VARCHAR(50) | | Category of hazard |
| severity | VARCHAR(10) | | low, medium, high, critical |
| confidence | DECIMAL(5,4) | | 0.0000 to 1.0000 |
| entities | JSONB | | Extracted entities |
| summary | TEXT | | AI-generated summary |
| model_version | VARCHAR(20) | NOT NULL | GPT model used |
| processing_time_ms | INTEGER | | Processing duration |
| created_at | TIMESTAMP | DEFAULT NOW() | Analysis timestamp |

**Indexes:**
- `idx_ai_analysis_report_id` ON `report_id`
- `idx_ai_analysis_hazard_type` ON `hazard_type`
- `idx_ai_analysis_severity` ON `severity`

**Constraints:**
```sql
ALTER TABLE ai_analysis ADD CONSTRAINT chk_severity CHECK (severity IN ('low', 'medium', 'high', 'critical'));
ALTER TABLE ai_analysis ADD CONSTRAINT chk_confidence CHECK (confidence >= 0 AND confidence <= 1);
```

**JSONB Entities Structure:**
```json
{
  "locations": [
    {"name": "Nairobi", "lat": -1.2921, "lng": 36.8219}
  ],
  "population_affected": 5000,
  "infrastructure": ["roads", "bridges"],
  "keywords": ["flooding", "evacuation"]
}
```

---

#### `incidents`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Incident title |
| description | TEXT | | Detailed description |
| hazard_type | VARCHAR(50) | NOT NULL | Primary hazard type |
| severity | VARCHAR(10) | NOT NULL | Incident severity |
| status | VARCHAR(20) | DEFAULT 'active' | active, contained, resolved, closed |
| latitude | DECIMAL(10,8) | NOT NULL | Center latitude |
| longitude | DECIMAL(11,8) | NOT NULL | Center longitude |
| location_name | VARCHAR(255) | | Location description |
| affected_radius_km | DECIMAL(10,2) | | Affected area radius |
| reporter_count | INTEGER | DEFAULT 1 | Number of contributing reporters |
| verified | BOOLEAN | DEFAULT FALSE | Verified by responder |
| verified_by | UUID | FK → users.id | Verifier user ID |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| resolved_at | TIMESTAMP | | Resolution timestamp |

**Indexes:**
- `idx_incidents_status` ON `status`
- `idx_incidents_severity` ON `severity`
- `idx_incidents_hazard_type` ON `hazard_type`
- `idx_incidents_location` ON `latitude, longitude`
- `idx_incidents_created_at` ON `created_at DESC`
- `idx_incidents_status_severity` ON `status, severity`

**Constraints:**
```sql
ALTER TABLE incidents ADD CONSTRAINT chk_incident_severity CHECK (severity IN ('low', 'medium', 'high', 'critical'));
ALTER TABLE incidents ADD CONSTRAINT chk_incident_status CHECK (status IN ('active', 'contained', 'resolved', 'closed'));
ALTER TABLE incidents ADD CONSTRAINT chk_incident_location_lat CHECK (latitude >= -90 AND latitude <= 90);
ALTER TABLE incidents ADD CONSTRAINT chk_incident_location_lng CHECK (longitude >= -180 AND longitude <= 180);
```

---

#### `incident_reports` (Junction Table)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| incident_id | UUID | FK → incidents.id, NOT NULL | Parent incident |
| report_id | UUID | FK → reports.id, NOT NULL | Contributed report |
| confidence_score | DECIMAL(5,4) | | How related (0-1) |
| created_at | TIMESTAMP | DEFAULT NOW() | Link timestamp |

**Primary Key:** `(incident_id, report_id)`

**Indexes:**
- `idx_incident_reports_report_id` ON `report_id`

---

#### `alerts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| incident_id | UUID | FK → incidents.id, NULLABLE | Related incident |
| title | VARCHAR(255) | NOT NULL | Alert title |
| message | TEXT | NOT NULL | Alert message |
| severity | VARCHAR(10) | NOT NULL | low, medium, high, critical |
| channel | VARCHAR(20) | NOT NULL | sms, email, whatsapp, push |
| target_audience | VARCHAR(50) | | all, responders, admins |
| recipients | JSONB | | Target recipient list |
| status | VARCHAR(20) | DEFAULT 'pending' | pending, sent, failed |
| sent_at | TIMESTAMP | | When alert was sent |
| created_by | UUID | FK → users.id | Creator user ID |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes:**
- `idx_alerts_incident_id` ON `incident_id`
- `idx_alerts_severity` ON `severity`
- `idx_alerts_channel` ON `channel`
- `idx_alerts_status` ON `status`
- `idx_alerts_created_at` ON `created_at DESC`

**Constraints:**
```sql
ALTER TABLE alerts ADD CONSTRAINT chk_alert_severity CHECK (severity IN ('low', 'medium', 'high', 'critical'));
ALTER TABLE alerts ADD CONSTRAINT chk_alert_channel CHECK (channel IN ('sms', 'email', 'whatsapp', 'push'));
ALTER TABLE alerts ADD CONSTRAINT chk_alert_status CHECK (status IN ('pending', 'sent', 'failed'));
```

---

#### `shelters`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Shelter name |
| description | TEXT | | Shelter description |
| latitude | DECIMAL(10,8) | NOT NULL | Location latitude |
| longitude | DECIMAL(11,8) | NOT NULL | Location longitude |
| address | VARCHAR(500) | | Full address |
| capacity | INTEGER | NOT NULL, CHECK > 0 | Max capacity |
| occupancy | INTEGER | DEFAULT 0, CHECK >= 0 | Current occupancy |
| status | VARCHAR(20) | DEFAULT 'available' | available, full, closed |
| facilities | JSONB | | Available facilities |
| contact_phone | VARCHAR(20) | | Contact phone |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_shelters_location` ON `latitude, longitude`
- `idx_shelters_status` ON `status`

**Constraints:**
```sql
ALTER TABLE shelters ADD CONSTRAINT chk_shelter_capacity CHECK (capacity > 0);
ALTER TABLE shelters ADD CONSTRAINT chk_shelter_occupancy CHECK (occupancy >= 0 AND occupancy <= capacity);
```

---

#### `hospitals`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Hospital name |
| description | TEXT | | Hospital description |
| latitude | DECIMAL(10,8) | NOT NULL | Location latitude |
| longitude | DECIMAL(11,8) | NOT NULL | Location longitude |
| address | VARCHAR(500) | | Full address |
| phone | VARCHAR(20) | | Contact phone |
| emergency_phone | VARCHAR(20) | | Emergency line |
| beds_total | INTEGER | | Total beds |
| beds_available | INTEGER | | Available beds |
| status | VARCHAR(20) | DEFAULT 'open' | open, limited, closed |
| services | JSONB | | Available services |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_hospitals_location` ON `latitude, longitude`
- `idx_hospitals_status` ON `status`

---

#### `trust_scores`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK → users.id, UNIQUE, NOT NULL | User reference |
| score | INTEGER | NOT NULL, CHECK 0-100 | Trust score |
| factors | JSONB | | Score breakdown |
| reason | TEXT | | Score change reason |
| updated_by | UUID | FK → users.id | Last updater |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_trust_scores_user_id` ON `user_id`

**Constraints:**
```sql
ALTER TABLE trust_scores ADD CONSTRAINT chk_trust_score CHECK (score >= 0 AND score <= 100);
```

---

#### `risk_scores`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| incident_id | UUID | FK → incidents.id, NOT NULL | Incident reference |
| score | DECIMAL(5,2) | NOT NULL | Risk score (0-100) |
| factors | JSONB | | Risk factors breakdown |
| model_version | VARCHAR(20) | | Model used |
| created_at | TIMESTAMP | DEFAULT NOW() | Calculation timestamp |

**Indexes:**
- `idx_risk_scores_incident_id` ON `incident_id`
- `idx_risk_scores_created_at` ON `created_at DESC`

---

#### `audit_logs`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| actor_id | UUID | FK → users.id, NULLABLE | User who performed action |
| actor_ip | VARCHAR(45) | | IP address |
| action | VARCHAR(50) | NOT NULL | Action performed |
| entity_type | VARCHAR(50) | | Entity affected |
| entity_id | UUID | | Entity ID |
| details | JSONB | | Additional details |
| status | VARCHAR(20) | | success, failure |
| error_message | TEXT | | Error details if failed |
| created_at | TIMESTAMP | DEFAULT NOW() | Action timestamp |

**Indexes:**
- `idx_audit_logs_actor_id` ON `actor_id`
- `idx_audit_logs_action` ON `action`
- `idx_audit_logs_entity` ON `entity_type, entity_id`
- `idx_audit_logs_created_at` ON `created_at DESC`

**Audit Actions:**
```sql
-- Auth
('login', 'logout', 'register', 'password_reset'),

-- Reports
('report_create', 'report_update', 'report_delete', 'report_verify'),

-- Incidents
('incident_create', 'incident_update', 'incident_resolve', 'incident_close'),

-- Alerts
('alert_create', 'alert_send', 'alert_fail'),

-- Admin
('user_create', 'user_update', 'user_deactivate', 'role_change');
```

---

## 3. Entity Relationships Summary

```
┌─────────────────┐       1:N       ┌─────────────────┐       N:1       ┌─────────────────┐
│     roles       │◄───────────────│     users       │────────────────▶│     roles       │
└─────────────────┘                └────────┬────────┘                 └─────────────────┘
                                             │
                                             │ 1:N
                                             ▼
┌─────────────────┐       1:1       ┌─────────────────┐                ┌─────────────────┐
│   ai_analysis   │◄───────────────│    reports      │────────────────▶│     users       │
└─────────────────┘                └────────┬────────┘                └─────────────────┘
                                             │                                    
                                             │ N:M (via incident_reports)          
                                             ▼                                    
┌─────────────────┐       1:N       ┌─────────────────┐                    
│  incident_reports│───────────────▶│    incidents    │                    
└─────────────────┘                └────────┬────────┘                    
                                             │                                    
                                             │ 1:N                                  
                                             ▼                                    
                                    ┌─────────────────┐                    
                                    │   risk_scores   │                    
                                    └─────────────────┘                    

┌─────────────────┐       1:N       ┌─────────────────┐
│  report_media   │─────────────────▶│    reports      │
└─────────────────┘                 └─────────────────┘

┌─────────────────┐       1:N       ┌─────────────────┐
│     alerts      │─────────────────▶│    incidents    │
└─────────────────┘                 └─────────────────┘

┌─────────────────┐       N:1       ┌─────────────────┐
│  trust_scores   │─────────────────▶│     users       │
└─────────────────┘                 └─────────────────┘

┌─────────────────┐       N:1       ┌─────────────────┐
│   audit_logs    │─────────────────▶│     users       │
└─────────────────┘                 └─────────────────┘
```

---

## 4. Database Triggers

### 4.1 Auto-update timestamp

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_reports_updated_at
    BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_incidents_updated_at
    BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### 4.2 Update reporter_count on incident

```sql
CREATE OR REPLACE FUNCTION update_incident_reporter_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE incidents SET reporter_count = reporter_count + 1 WHERE id = NEW.incident_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE incidents SET reporter_count = reporter_count - 1 WHERE id = OLD.incident_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_incident_report_count
    AFTER INSERT OR DELETE ON incident_reports
    FOR EACH ROW EXECUTE FUNCTION update_incident_reporter_count();
```

### 4.3 Validate occupancy

```sql
CREATE OR REPLACE FUNCTION check_shelter_occupancy()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.occupancy > NEW.capacity THEN
        RAISE EXCEPTION 'Occupancy (%) cannot exceed capacity (%)', NEW.occupancy, NEW.capacity;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_shelter_occupancy
    BEFORE UPDATE ON shelters
    FOR EACH ROW EXECUTE FUNCTION check_shelter_occupancy();
```

---

## 5. Migrations

### Migration File Structure

```
backend/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_ai_analysis.py
│       └── 003_add_audit_logs.py
```

### Initial Migration (001)

```python
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create roles table
    op.create_table('roles',
        sa.Column('id', UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_roles_name', 'roles', ['name'])

    # Seed roles
    op.execute("""
        INSERT INTO roles (name, description) VALUES
        ('citizen', 'Community member who can submit reports'),
        ('responder', 'Emergency responder who can manage incidents'),
        ('analyst', 'AI/ICPAC analyst who can view analytics'),
        ('admin', 'System administrator with full access');
    """)

    # Create users table
    op.create_table('users',
        sa.Column('id', UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role_id', UUID(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('phone'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'])
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_phone', 'users', ['phone'])
    op.create_index('idx_users_role_id', 'users', ['role_id'])

    # Continue with other tables...
    # (full migration in actual implementation)

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('risk_scores')
    op.drop_table('trust_scores')
    op.drop_table('hospitals')
    op.drop_table('shelters')
    op.drop_table('alerts')
    op.drop_table('incident_reports')
    op.drop_table('incidents')
    op.drop_table('ai_analysis')
    op.drop_table('report_media')
    op.drop_table('reports')
    op.drop_table('users')
    op.drop_table('roles')
```

---

## 6. Row-Level Security (RLS)

Enable RLS for Supabase:

```sql
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Users: Users can read all, update only own
CREATE POLICY "Users read all" ON users FOR SELECT USING (true);
CREATE POLICY "Users update own" ON users FOR UPDATE USING (auth.uid() = id);

-- Reports: Citizens create, read all, update own
CREATE POLICY "Reports read all" ON reports FOR SELECT USING (true);
CREATE POLICY "Reports create" ON reports FOR INSERT WITH CHECK (auth.uid() = reporter_id OR reporter_id IS NULL);
CREATE POLICY "Reports update own" ON reports FOR UPDATE USING (auth.uid() = reporter_id);

-- Incidents: Responders update, Analysts read
CREATE POLICY "Incidents read all" ON incidents FOR SELECT USING (true);
CREATE POLICY "Incidents responder update" ON incidents FOR UPDATE USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role_id IN (
        SELECT id FROM roles WHERE name IN ('responder', 'admin')
    ))
);
```

---

## 7. Performance Considerations

### 7.1 Partitioning Strategy

For large-scale deployment, consider:

```sql
-- Partition reports by month
CREATE TABLE reports_partitioned (
    LIKE reports INCLUDING ALL
) PARTITION BY RANGE (created_at);

CREATE TABLE reports_2026_06 PARTITION OF reports_partitioned
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

### 7.2 Connection Pooling

```yaml
# PgBouncer config
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
```

### 7.3 Query Optimization

Use EXPLAIN ANALYZE for critical queries:

```sql
EXPLAIN ANALYZE
SELECT i.*, COUNT(ir.report_id) as report_count
FROM incidents i
LEFT JOIN incident_reports ir ON i.id = ir.incident_id
WHERE i.status = 'active' AND i.severity IN ('high', 'critical')
GROUP BY i.id
ORDER BY i.created_at DESC
LIMIT 20;
```

---

*Document Version: 1.0*
*Last Updated: 2026-06-24*