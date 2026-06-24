from sqlalchemy.orm import Session
from app.models import Incident, RiskScore
from datetime import datetime


class IncidentService:
    def __init__(self, db: Session):
        self.db = db

    async def calculate_risk_score(self, incident: Incident) -> RiskScore:
        severity_scores = {
            "low": 10,
            "medium": 30,
            "high": 60,
            "critical": 90
        }

        base_score = severity_scores.get(incident.severity, 30)

        reporter_factor = min(incident.reporter_count * 2, 20)

        risk_score = min(base_score + reporter_factor, 100)

        factors = {
            "severity": base_score,
            "reporter_count": reporter_factor,
            "location": 10 if incident.location_name else 0,
            "time_decay": 0
        }

        risk = RiskScore(
            incident_id=incident.id,
            score=risk_score,
            factors=factors,
            model_version="1.0"
        )

        self.db.add(risk)
        self.db.commit()

        return risk

    async def link_report_to_incident(self, report, incident: Incident) -> None:
        from app.models import IncidentReport

        existing = self.db.query(IncidentReport).filter(
            IncidentReport.report_id == report.id
        ).first()

        if existing:
            return

        ir = IncidentReport(
            incident_id=incident.id,
            report_id=report.id,
            confidence_score=0.8
        )

        self.db.add(ir)

        incident.reporter_count = (incident.reporter_count or 0) + 1

        self.db.commit()

        await self.calculate_risk_score(incident)