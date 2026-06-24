# API Requirements

All APIs must be OpenAPI compliant.

Base URL:

/api/v1

---

Authentication

POST /auth/login

POST /auth/register

POST /auth/logout

GET /auth/me

---

Reports

POST /reports

GET /reports

GET /reports/{id}

PUT /reports/{id}

DELETE /reports/{id}

---

Incidents

POST /incidents

GET /incidents

GET /incidents/{id}

PUT /incidents/{id}

DELETE /incidents/{id}

---

Alerts

POST /alerts

GET /alerts

GET /alerts/{id}

---

Analytics

GET /analytics

GET /analytics/risk

GET /analytics/incidents

---

Webhooks

POST /webhooks/sms

POST /webhooks/whatsapp

POST /webhooks/voice

---

System

GET /health

GET /metrics

---

Requirements

* Validation
* Pagination
* Filtering
* Sorting
* OpenAPI docs
* Error handling

