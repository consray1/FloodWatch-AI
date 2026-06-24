# Database Requirements

Design a normalized PostgreSQL schema.

Required Tables:

## users

* id
* name
* email
* phone
* role_id
* created_at

## roles

* id
* name

## reports

* id
* source
* reporter_id
* raw_text
* created_at

## report_media

* id
* report_id
* media_url
* media_type

## ai_analysis

* id
* report_id
* hazard_type
* severity
* confidence
* summary

## incidents

* id
* title
* description
* severity
* latitude
* longitude
* status

## incident_reports

* incident_id
* report_id

## alerts

* id
* title
* message
* severity
* channel

## shelters

* id
* name
* capacity
* occupancy

## hospitals

* id
* name
* latitude
* longitude

## trust_scores

* id
* user_id
* score

## risk_scores

* id
* incident_id
* score

## audit_logs

* id
* actor_id
* action
* created_at

---

Requirements:

* Foreign keys
* Indexes
* Constraints
* Migrations
* ERD generation

