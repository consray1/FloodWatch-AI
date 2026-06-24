from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models import Report, Incident, Alert
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
async def get_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    total_reports = db.query(func.count(Report.id)).scalar()
    reports_today = db.query(func.count(Report.id)).filter(
        func.date(Report.created_at) == today
    ).scalar()

    total_incidents = db.query(func.count(Incident.id)).scalar()
    active_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "active"
    ).scalar()

    critical_alerts = db.query(func.count(Alert.id)).filter(
        Alert.severity == "critical",
        Alert.status == "pending"
    ).scalar()

    reports_by_day = db.query(
        func.date(Report.created_at).label("date"),
        func.count(Report.id).label("count")
    ).filter(
        Report.created_at >= week_ago
    ).group_by(func.date(Report.created_at)).all()

    hazard_stats = db.query(
        Report.source,
        func.count(Report.id).label("count")
    ).group_by(Report.source).all()

    severity_stats = db.query(
        Incident.severity,
        func.count(Incident.id).label("count")
    ).filter(
        Incident.status == "active"
    ).group_by(Incident.severity).all()

    return {
        "overview": {
            "total_reports": total_reports,
            "reports_today": reports_today,
            "total_incidents": total_incidents,
            "active_incidents": active_incidents,
            "critical_alerts": critical_alerts
        },
        "trends": {
            "reports_last_7_days": [r.count for r in reports_by_day]
        },
        "top_hazards": [{"type": h.source, "count": h.count} for h in hazard_stats],
        "severity_distribution": {s.severity: s.count for s in severity_stats}
    }


@router.get("/risk")
async def get_risk_analytics(
    incident_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.models import RiskScore

    query = db.query(RiskScore)

    if incident_id:
        query = query.filter(RiskScore.incident_id == incident_id)

    risk_scores = query.order_by(RiskScore.created_at.desc()).limit(100).all()

    risk_trends = [
        {
            "date": r.created_at.isoformat(),
            "score": float(r.score)
        }
        for r in risk_scores
    ]

    return {
        "risk_trends": risk_trends,
        "high_risk_areas": [],
        "risk_factors": {}
    }


@router.get("/incidents")
async def get_incident_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from sqlalchemy import extract

    total = db.query(func.count(Incident.id)).scalar()
    by_status = db.query(
        Incident.status,
        func.count(Incident.id).label("count")
    ).group_by(Incident.status).all()

    by_hazard = db.query(
        Incident.hazard_type,
        func.count(Incident.id).label("count")
    ).group_by(Incident.hazard_type).all()

    by_severity = db.query(
        Incident.severity,
        func.count(Incident.id).label("count")
    ).group_by(Incident.severity).all()

    return {
        "summary": {
            "total": total,
            "by_status": {s.status: s.count for s in by_status},
            "by_hazard": {h.hazard_type: h.count for h in by_hazard},
            "by_severity": {s.severity: s.count for s in by_severity}
        }
    }