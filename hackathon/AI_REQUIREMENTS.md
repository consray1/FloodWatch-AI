# AI Requirements

Models

Primary:
GPT-5.5

Speech:
Whisper

---

Task 1

Hazard Classification

Input:

Community report

Output:

{
hazard_type,
severity,
confidence
}

---

Task 2

Entity Extraction

Extract:

* locations
* affected population
* infrastructure impact

---

Task 3

Incident Summarization

Generate concise operational summaries.

---

Task 4

Duplicate Detection

Determine if reports belong to existing incidents.

---

Task 5

Trust Score Assistance

Recommend trust score updates.

---

Requirements

* JSON responses only
* Schema validation
* Retry handling
* Fallback handling
* Logging

