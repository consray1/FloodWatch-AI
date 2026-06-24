# FloodWatch AI - API Contracts

**Version:** 1.0.0
**Base URL:** `/api/v1`
**OpenAPI Version:** 3.0.3
**Authentication:** Bearer JWT (Supabase)

---

## 1. Authentication

### 1.1 POST /auth/register

Register a new user account.

**Request:**
```yaml
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+254712345678",
  "password": "SecureP@ss123"
}
```

**Response (201):**
```yaml
{
  "id": "uuid",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+254712345678",
  "role": "citizen",
  "created_at": "2026-06-24T10:00:00Z"
}
```

**Errors:**
- 400: Invalid input
- 409: Email already registered

---

### 1.2 POST /auth/login

Authenticate user and receive tokens.

**Request:**
```yaml
{
  "email": "jane@example.com",
  "password": "SecureP@ss123"
}
```

**Response (200):**
```yaml
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Errors:**
- 400: Invalid input
- 401: Invalid credentials
- 429: Too many attempts

---

### 1.3 POST /auth/logout

Invalidate current session.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204):** No content

**Errors:**
- 401: Unauthorized

---

### 1.4 GET /auth/me

Get current user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```yaml
{
  "id": "uuid",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+254712345678",
  "role": "citizen",
  "is_verified": true,
  "trust_score": 85,
  "created_at": "2026-06-24T10:00:00Z",
  "last_login": "2026-06-24T14:30:00Z"
}
```

**Errors:**
- 401: Unauthorized

---

### 1.5 POST /auth/refresh

Refresh access token.

**Request:**
```yaml
{
  "refresh_token": "eyJ..."
}
```

**Response (200):**
```yaml
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Errors:**
- 401: Invalid refresh token

---

## 2. Reports

### 2.1 POST /reports

Submit a new report.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data (if includes media)
```

**Request (JSON):**
```yaml
{
  "source": "web",
  "raw_text": "Heavy flooding reported on Mombasa Road near Kenol. Water levels rising rapidly.",
  "location_lat": -1.2921,
  "location_lng": 36.8219,
  "location_name": "Mombasa Road, Nairobi"
}
```

**Request (multipart/form-data):**
```
raw_text: "Heavy flooding reported..."
location_lat: -1.2921
location_lng: 36.8219
location_name: "Mombasa Road"
media[]: (file upload, optional)
```

**Response (201):**
```yaml
{
  "id": "uuid",
  "source": "web",
  "status": "pending",
  "raw_text": "Heavy flooding reported on Mombasa Road...",
  "location": {
    "lat": -1.2921,
    "lng": 36.8219,
    "name": "Mombasa Road, Nairobi"
  },
  "media": [
    {
      "id": "uuid",
      "url": "https://storage.supabase.co/reports/abc.jpg",
      "type": "image"
    }
  ],
  "reporter": {
    "id": "uuid",
    "name": "Jane Doe"
  },
  "created_at": "2026-06-24T10:00:00Z"
}
```

**Errors:**
- 400: Invalid input / validation error
- 401: Unauthorized

---

### 2.2 GET /reports

List reports with filtering and pagination.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Page number |
| limit | int | 20 | Items per page (max 100) |
| source | string | | Filter by source |
| status | string | | pending, analyzed, verified, dismissed |
| hazard_type | string | | Filter by AI-detected hazard |
| severity | string | | low, medium, high, critical |
| reporter_id | uuid | | Filter by reporter |
| created_after | datetime | | Filter by date |
| created_before | datetime | | Filter by date |
| location_within | string | | lat,lng,radius_km |
| sort | string | created_at | Sort field |
| order | string | desc | asc or desc |

**Response (200):**
```yaml
{
  "data": [
    {
      "id": "uuid",
      "source": "web",
      "raw_text": "Heavy flooding reported...",
      "location": {
        "lat": -1.2921,
        "lng": 36.8219,
        "name": "Mombasa Road"
      },
      "status": "analyzed",
      "ai_analysis": {
        "hazard_type": "flood",
        "severity": "high",
        "confidence": 0.94
      },
      "reporter": {
        "id": "uuid",
        "name": "Jane Doe"
      },
      "created_at": "2026-06-24T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

### 2.3 GET /reports/{id}

Get single report details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```yaml
{
  "id": "uuid",
  "source": "web",
  "raw_text": "Heavy flooding reported on Mombasa Road near Kenol.",
  "location": {
    "lat": -1.2921,
    "lng": 36.8219,
    "name": "Mombasa Road, Nairobi"
  },
  "status": "analyzed",
  "language": "en",
  "media": [...],
  "ai_analysis": {
    "id": "uuid",
    "hazard_type": "flood",
    "hazard_category": "flash_flood",
    "severity": "high",
    "confidence": 0.94,
    "entities": {
      "locations": [{"name": "Mombasa Road", "lat": -1.2921, "lng": 36.8219}],
      "population_affected": 5000,
      "infrastructure": ["roads"],
      "keywords": ["flooding", "water_levels"]
    },
    "summary": "Flash flooding reported on Mombasa Road. Approximately 5000 people affected. Roads may be impassable.",
    "model_version": "gpt-5.5-2026",
    "processing_time_ms": 2350
  },
  "incident": {
    "id": "uuid",
    "title": "Mombasa Road Flooding",
    "severity": "high"
  },
  "reporter": {
    "id": "uuid",
    "name": "Jane Doe",
    "trust_score": 85
  },
  "created_at": "2026-06-24T10:00:00Z"
}
```

**Errors:**
- 404: Report not found

---

### 2.4 PUT /reports/{id}

Update a report (own reports only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```yaml
{
  "raw_text": "Updated information...",
  "location_lat": -1.2930,
  "location_lng": 36.8225,
  "location_name": "Updated location"
}
```

**Response (200):** Updated report object

**Errors:**
- 400: Invalid input
- 401: Unauthorized
- 403: Not your report
- 404: Report not found

---

### 2.5 DELETE /reports/{id}

Delete a report (own reports or admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204):** No content

**Errors:**
- 401: Unauthorized
- 403: Not authorized
- 404: Report not found

---

## 3. Incidents

### 3.1 POST /incidents

Create a new incident (Responder/Admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```yaml
{
  "title": "Mombasa Road Flooding",
  "description": "Major flash flooding event affecting traffic and local residents.",
  "hazard_type": "flood",
  "severity": "high",
  "latitude": -1.2921,
  "longitude": 36.8219,
  "location_name": "Mombasa Road, Nairobi",
  "affected_radius_km": 2.5
}
```

**Response (201):**
```yaml
{
  "id": "uuid",
  "title": "Mombasa Road Flooding",
  "description": "Major flash flooding event...",
  "hazard_type": "flood",
  "severity": "high",
  "status": "active",
  "location": {
    "lat": -1.2921,
    "lng": 36.8219,
    "name": "Mombasa Road, Nairobi"
  },
  "affected_radius_km": 2.5,
  "reporter_count": 0,
  "verified": false,
  "risk_score": null,
  "created_at": "2026-06-24T10:00:00Z"
}
```

**Errors:**
- 400: Invalid input
- 401: Unauthorized
- 403: Insufficient permissions

---

### 3.2 GET /incidents

List incidents with filtering.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Page number |
| limit | int | 20 | Items per page |
| status | string | | active, contained, resolved, closed |
| severity | string | | low, medium, high, critical |
| hazard_type | string | | flood, landslide, storm |
| verified | boolean | | Filter by verification |
| created_after | datetime | | Filter by date |
| location_within | string | | lat,lng,radius_km |
| sort | string | created_at | Sort field |
| order | string | desc | asc or desc |

**Response (200):**
```yaml
{
  "data": [
    {
      "id": "uuid",
      "title": "Mombasa Road Flooding",
      "hazard_type": "flood",
      "severity": "high",
      "status": "active",
      "location": {
        "lat": -1.2921,
        "lng": 36.8219,
        "name": "Mombasa Road"
      },
      "reporter_count": 15,
      "verified": true,
      "risk_score": 78.5,
      "created_at": "2026-06-24T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 25,
    "total_pages": 2
  }
}
```

---

### 3.3 GET /incidents/{id}

Get incident details with reports.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```yaml
{
  "id": "uuid",
  "title": "Mombasa Road Flooding",
  "description": "Major flash flooding event...",
  "hazard_type": "flood",
  "severity": "high",
  "status": "active",
  "location": {
    "lat": -1.2921,
    "lng": 36.8219,
    "name": "Mombasa Road"
  },
  "affected_radius_km": 2.5,
  "reporter_count": 15,
  "verified": true,
  "verified_by": {
    "id": "uuid",
    "name": "John Responder"
  },
  "reports": [
    {
      "id": "uuid",
      "raw_text": "Heavy flooding...",
      "source": "web",
      "created_at": "2026-06-24T10:00:00Z"
    }
  ],
  "alerts": [...],
  "risk_score": {
    "score": 78.5,
    "factors": {
      "severity": 30,
      "population_density": 25,
      "infrastructure_impact": 15,
      "report_frequency": 8.5
    }
  },
  "nearby_shelters": [
    {
      "id": "uuid",
      "name": "Kenya High School Shelter",
      "distance_km": 1.2,
      "capacity": 500,
      "occupancy": 230
    }
  ],
  "nearby_hospitals": [...],
  "created_at": "2026-06-24T10:00:00Z",
  "updated_at": "2026-06-24T14:00:00Z"
}
```

---

### 3.4 PUT /incidents/{id}

Update incident (Responder/Admin only).

**Request:**
```yaml
{
  "title": "Updated title",
  "description": "Updated description",
  "severity": "critical",
  "status": "contained",
  "verified": true
}
```

**Response (200):** Updated incident object

**Errors:**
- 400: Invalid input
- 401: Unauthorized
- 403: Insufficient permissions
- 404: Incident not found

---

### 3.5 DELETE /incidents/{id}

Delete incident (Admin only).

**Response (204):** No content

**Errors:**
- 401: Unauthorized
- 403: Admin access required
- 404: Incident not found

---

## 4. Alerts

### 4.1 POST /alerts

Create a new alert (Responder/Admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```yaml
{
  "incident_id": "uuid",
  "title": "Flood Warning: Mombasa Road",
  "message": "Severe flooding expected in the next 2 hours. Evacuate immediately.",
  "severity": "critical",
  "channel": "sms",
  "target_audience": "all"
}
```

**Response (201):**
```yaml
{
  "id": "uuid",
  "incident_id": "uuid",
  "title": "Flood Warning: Mombasa Road",
  "message": "Severe flooding expected...",
  "severity": "critical",
  "channel": "sms",
  "target_audience": "all",
  "status": "pending",
  "recipients_count": 1250,
  "created_by": {
    "id": "uuid",
    "name": "John Responder"
  },
  "created_at": "2026-06-24T10:00:00Z"
}
```

**Errors:**
- 400: Invalid input
- 401: Unauthorized
- 403: Insufficient permissions

---

### 4.2 GET /alerts

List alerts.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Page number |
| limit | int | 20 | Items per page |
| status | string | | pending, sent, failed |
| severity | string | | low, medium, high, critical |
| channel | string | | sms, email, whatsapp, push |
| incident_id | uuid | | Filter by incident |

**Response (200):**
```yaml
{
  "data": [
    {
      "id": "uuid",
      "title": "Flood Warning: Mombasa Road",
      "severity": "critical",
      "channel": "sms",
      "status": "sent",
      "sent_at": "2026-06-24T10:05:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### 4.3 GET /alerts/{id}

Get alert details.

**Response (200):**
```yaml
{
  "id": "uuid",
  "incident_id": "uuid",
  "title": "Flood Warning: Mombasa Road",
  "message": "Severe flooding expected...",
  "severity": "critical",
  "channel": "sms",
  "target_audience": "all",
  "status": "sent",
  "sent_at": "2026-06-24T10:05:00Z",
  "recipients": {
    "total": 1250,
    "delivered": 1200,
    "failed": 50
  },
  "created_by": {...},
  "created_at": "2026-06-24T10:00:00Z"
}
```

---

## 5. Analytics

### 5.1 GET /analytics

Get dashboard analytics summary.

**Response (200):**
```yaml
{
  "overview": {
    "total_reports": 1250,
    "reports_today": 45,
    "total_incidents": 85,
    "active_incidents": 12,
    "critical_alerts": 3
  },
  "trends": {
    "reports_last_7_days": [120, 135, 98, 145, 162, 140, 145],
    "incidents_by_day": [...]
  },
  "top_hazards": [
    {"type": "flood", "count": 45},
    {"type": "storm", "count": 12},
    {"type": "landslide", "count": 5}
  ],
  "severity_distribution": {
    "critical": 5,
    "high": 15,
    "medium": 35,
    "low": 30
  }
}
```

---

### 5.2 GET /analytics/risk

Get risk score analytics.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| incident_id | uuid | Specific incident |
| start_date | date | Date range start |
| end_date | date | Date range end |

**Response (200):**
```yaml
{
  "risk_trends": [
    {
      "date": "2026-06-24",
      "avg_risk_score": 65.5,
      "max_risk_score": 92.0,
      "incidents_count": 12
    }
  ],
  "high_risk_areas": [
    {
      "location": "Mombasa Road",
      "avg_risk_score": 78.5,
      "incident_count": 5
    }
  ],
  "risk_factors": {
    "infrastructure": 35,
    "population_density": 28,
    "historical_frequency": 22,
    "response_time": 15
  }
}
```

---

### 5.3 GET /analytics/incidents

Get incident analytics.

**Response (200):**
```yaml
{
  "summary": {
    "total": 85,
    "active": 12,
    "contained": 25,
    "resolved": 48,
    "avg_resolution_time_hours": 48
  },
  "by_hazard_type": [
    {"type": "flood", "count": 45, "avg_resolution_hours": 36},
    {"type": "storm", "count": 20, "avg_resolution_hours": 24}
  ],
  "by_severity": [
    {"severity": "critical", "count": 8, "avg_resolution_hours": 12},
    {"severity": "high", "count": 22, "avg_resolution_hours": 36}
  ],
  "geographic_distribution": [
    {"region": "Nairobi", "count": 30},
    {"region": "Mombasa", "count": 25}
  ]
}
```

---

## 6. Webhooks

### 6.1 POST /webhooks/sms

Receive SMS reports from Twilio.

**Request (from Twilio):**
```
POSTBody (application/x-www-form-urlencoded):
  From: +254712345678
  Body: Heavy flooding on Mombasa Road
```

**Response (200):** TwiML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Thank you for your report. We have received your flood warning and are analyzing it now.</Message>
</Response>
```

**Errors:**
- 400: Invalid request
- 403: Invalid signature

---

### 6.2 POST /webhooks/whatsapp

Receive WhatsApp reports from Twilio.

**Request (from Twilio):**
```json
{
  "From": "whatsapp:+254712345678",
  "Body": "Flooding in Kisumu near the stadium"
}
```

**Response (200):**
```json
{
  "status": "received",
  "report_id": "uuid"
}
```

---

### 6.3 POST /webhooks/voice

Receive voice reports (transcribed by Twilio + Whisper).

**Request (from Twilio):**
```
POSTBody:
  From: +254712345678
  RecordingUrl: https://api.twilio.com/recordings/xxx
  TranscriptionText: "There's a lot of water on the road near the market"
```

**Response (200):** TwiML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Thank you for your report. We have received your flood warning and are analyzing it now.</Message>
</Response>
```

---

### 6.4 POST /webhooks/icpac

Receive external alerts from ICPAC.

**Headers:**
```
X-ICPAC-Signature: <HMAC signature>
X-ICPAC-Timestamp: <timestamp>
```

**Request:**
```yaml
{
  "alert_id": "ICPAC-2026-001",
  "alert_type": "flood_warning",
  "severity": "high",
  "headline": "Heavy rainfall expected in Nairobi region",
  "description": "ICPAC forecasts heavy rainfall...",
  "effective_from": "2026-06-24T12:00:00Z",
  "effective_until": "2026-06-25T12:00:00Z",
  "affected_areas": [
    {"name": "Nairobi", "lat": -1.2921, "lng": 36.8219}
  ],
  "recommendations": ["Evacuate low-lying areas", "Avoid travel"]
}
```

**Response (200):**
```yaml
{
  "status": "received",
  "internal_incident_id": "uuid" // if auto-created
}
```

**Errors:**
- 400: Invalid payload
- 401: Invalid signature
- 403: Timestamp expired

---

## 7. System

### 7.1 GET /health

Health check endpoint.

**Response (200):**
```yaml
{
  "status": "healthy",
  "timestamp": "2026-06-24T10:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "up",
    "ai_service": "up",
    "storage": "up"
  }
}
```

---

### 7.2 GET /metrics

Prometheus-format metrics.

**Response (200):**
```
# HELP floodwatch_reports_total Total number of reports
# TYPE floodwatch_reports_total counter
floodwatch_reports_total{source="web"} 450

# HELP floodwatch_incidents_active Current active incidents
# TYPE floodwatch_incidents_active gauge
floodwatch_incidents_active 12

# HELP floodwatch_ai_latency_seconds AI analysis latency
# TYPE floodwatch_ai_latency_seconds histogram
floodwatch_ai_latency_seconds_bucket{le="1"} 150
```

---

## 8. Error Responses

All errors follow this format:

```yaml
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "uuid"
  }
}
```

**Error Codes:**
| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid request body |
| 400 | INVALID_INPUT | Invalid parameter value |
| 401 | UNAUTHORIZED | Missing or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |
| 403 | INVALID_SIGNATURE | Webhook signature invalid |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource already exists |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |

---

## 9. Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| POST /auth/* | 10 | 1 minute |
| POST /reports | 20 | 1 minute |
| GET /reports | 100 | 1 minute |
| POST /incidents | 10 | 1 minute |
| POST /alerts | 10 | 1 minute |
| Webhooks | 1000 | 1 minute |

Rate limit headers included in response:
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 1719228060
```

---

## 10. Pagination

Default pagination:
```yaml
page: 1
limit: 20
max_limit: 100
```

Response wrapper:
```yaml
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 11. OpenAPI Specification

Full OpenAPI 3.0 spec available at `/api/v1/docs`

Swagger UI: `GET /api/v1/docs`
ReDoc: `GET /api/v1/redoc`

---

*Document Version: 1.0*
*Last Updated: 2026-06-24*