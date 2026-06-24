from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.models import Incident, User, Report, IncidentReport, RiskScore, Alert
from app.schemas import IncidentCreate, IncidentUpdate, IncidentResponse, IncidentDetailResponse, IncidentListResponse
from app.api.v1.deps import get_current_user, require_responder
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["incidents"])


def build_incident_response(incident: Incident) -> IncidentResponse:
    risk_score = None
    if incident.risk_scores:
        latest = sorted(incident.risk_scores, key=lambda x: x.created_at, reverse=True)[0]
        risk_score = float(latest.score) if latest else None

    return IncidentResponse(
        id=incident.id,
        title=incident.title,
        description=incident.description,
        hazard_type=incident.hazard_type,
        severity=incident.severity,
        status=incident.status,
        location={
            "lat": float(incident.latitude),
            "lng": float(incident.longitude),
            "name": incident.location_name
        },
        affected_radius_km=float(incident.affected_radius_km) if incident.affected_radius_km else None,
        reporter_count=incident.reporter_count,
        verified=incident.verified,
        risk_score=risk_score,
        created_at=incident.created_at,
        updated_at=incident.updated_at
    )


@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_responder)
):
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        hazard_type=incident_data.hazard_type,
        severity=incident_data.severity,
        latitude=incident_data.latitude,
        longitude=incident_data.longitude,
        location_name=incident_data.location_name,
        affected_radius_km=incident_data.affected_radius_km
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    service = IncidentService(db)
    await service.calculate_risk_score(incident)

    return build_incident_response(incident)


@router.get("", response_model=IncidentListResponse)
async def list_incidents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    hazard_type: Optional[str] = None,
    verified: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Incident).options(
        joinedload(Incident.risk_scores)
    )

    if status:
        query = query.filter(Incident.status == status)
    if severity:
        query = query.filter(Incident.severity == severity)
    if hazard_type:
        query = query.filter(Incident.hazard_type == hazard_type)
    if verified is not None:
        query = query.filter(Incident.verified == verified)

    total = query.count()
    incidents = query.order_by(Incident.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return IncidentListResponse(
        data=[build_incident_response(i) for i in incidents],
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )


@router.get("/{incident_id}", response_model=IncidentDetailResponse)
async def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).options(
        joinedload(Incident.risk_scores),
        joinedload(Incident.incident_reports).joinedload(IncidentReport.report),
        joinedload(Incident.alerts),
        joinedload(Incident.verified_by)
    ).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    risk_score = None
    if incident.risk_scores:
        latest = sorted(incident.risk_scores, key=lambda x: x.created_at, reverse=True)[0]
        risk_score = {
            "score": float(latest.score),
            "factors": latest.factors
        }

    return IncidentDetailResponse(
        id=incident.id,
        title=incident.title,
        description=incident.description,
        hazard_type=incident.hazard_type,
        severity=incident.severity,
        status=incident.status,
        location={
            "lat": float(incident.latitude),
            "lng": float(incident.longitude),
            "name": incident.location_name
        },
        affected_radius_km=float(incident.affected_radius_km) if incident.affected_radius_km else None,
        reporter_count=incident.reporter_count,
        verified=incident.verified,
        risk_score=float(risk_score["score"]) if risk_score else None,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
        reports=[{"id": r.report.id, "raw_text": r.report.raw_text, "source": r.report.source} for r in incident.incident_reports],
        alerts=[{"id": a.id, "title": a.title, "severity": a.severity} for a in incident.alerts],
        nearby_shelters=[],
        nearby_hospitals=[],
        verified_by={"id": incident.verified_by.id, "name": incident.verified_by.name} if incident.verified_by else None
    )


@router.put("/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    incident_id: UUID,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_responder)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if incident_data.title is not None:
        incident.title = incident_data.title
    if incident_data.description is not None:
        incident.description = incident_data.description
    if incident_data.severity is not None:
        incident.severity = incident_data.severity
    if incident_data.status is not None:
        incident.status = incident_data.status
        if incident_data.status == "resolved":
            from datetime import datetime
            incident.resolved_at = datetime.utcnow()
    if incident_data.verified is not None:
        incident.verified = incident_data.verified
        if incident_data.verified:
            incident.verified_by = current_user.id

    db.commit()
    db.refresh(incident)

    return build_incident_response(incident)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(incident)
    db.commit()