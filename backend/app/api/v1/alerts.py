from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models import Alert, User, Incident
from app.schemas import AlertCreate, AlertResponse, AlertDetailResponse, AlertListResponse
from app.api.v1.deps import get_current_user, require_responder
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_responder)
):
    if alert_data.incident_id:
        incident = db.query(Incident).filter(Incident.id == alert_data.incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

    alert = Alert(
        incident_id=alert_data.incident_id,
        title=alert_data.title,
        message=alert_data.message,
        severity=alert_data.severity,
        channel=alert_data.channel,
        target_audience=alert_data.target_audience or "all",
        created_by=current_user.id
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    service = AlertService(db)
    recipients_count = await service.send_alert(alert)

    return AlertResponse(
        id=alert.id,
        incident_id=alert.incident_id,
        title=alert.title,
        severity=alert.severity,
        channel=alert.channel,
        status=alert.status,
        recipients_count=recipients_count,
        created_by={"id": current_user.id, "name": current_user.name},
        created_at=alert.created_at
    )


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    channel: Optional[str] = None,
    incident_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Alert).options(joinedload(Alert.created_by))

    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if channel:
        query = query.filter(Alert.channel == channel)
    if incident_id:
        query = query.filter(Alert.incident_id == incident_id)

    total = query.count()
    alerts = query.order_by(Alert.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return AlertListResponse(
        data=[
            AlertResponse(
                id=a.id,
                incident_id=a.incident_id,
                title=a.title,
                severity=a.severity,
                channel=a.channel,
                status=a.status,
                sent_at=a.sent_at,
                created_by={"id": a.created_by.id, "name": a.created_by.name} if a.created_by else None,
                created_at=a.created_at
            )
            for a in alerts
        ],
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )


@router.get("/{alert_id}", response_model=AlertDetailResponse)
async def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = db.query(Alert).options(joinedload(Alert.created_by)).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return AlertDetailResponse(
        id=alert.id,
        incident_id=alert.incident_id,
        title=alert.title,
        message=alert.message,
        severity=alert.severity,
        channel=alert.channel,
        status=alert.status,
        recipients=alert.recipients,
        sent_at=alert.sent_at,
        created_by={"id": alert.created_by.id, "name": alert.created_by.name} if alert.created_by else None,
        created_at=alert.created_at
    )