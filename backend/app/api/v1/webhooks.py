from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
import hmac
import hashlib
import time
from datetime import datetime
from app.core.database import get_db
from app.core.config import settings
from app.models import Report
from app.schemas import ReportCreate
from app.api.v1.deps import get_current_user_optional
from app.services.report_service import ReportService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_twilio_signature(request: Request) -> bool:
    if not settings.TWILIO_AUTH_TOKEN:
        return True

    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    params = dict(request.query_params)

    validation_string = "".join([url] + [f"{k}{v}" for k, v in sorted(params.items())])
    expected_signature = hmac.new(
        settings.TWILIO_AUTH_TOKEN.encode(),
        validation_string.encode(),
        hashlib.sha1
    ).digest().hex()

    return hmac.compare_digest(signature, expected_signature)


def verify_icpac_signature(request: Request, body: dict) -> bool:
    timestamp = request.headers.get("X-ICPAC-Timestamp", "")
    signature = request.headers.get("X-ICPAC-Signature", "")

    if not timestamp or not signature:
        return False

    try:
        request_time = int(timestamp)
        current_time = int(time.time())
        if abs(current_time - request_time) > 300:
            return False
    except ValueError:
        return False

    message = f"{timestamp}:{body.get('alert_id', '')}"
    expected = hmac.new(
        settings.TWILIO_WEBHOOK_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


@router.post("/sms")
async def receive_sms(
    request: Request,
    From: str,
    Body: str,
    db: Session = Depends(get_db)
):
    if not verify_twilio_signature(request):
        raise HTTPException(status_code=403, detail="Invalid signature")

    report = Report(
        source="sms",
        raw_text=Body.strip(),
        phone=From
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    service = ReportService(db)
    await service.trigger_ai_analysis(report)

    return {"status": "received", "report_id": str(report.id)}


@router.post("/whatsapp")
async def receive_whatsapp(
    request: Request,
    From: str,
    Body: str,
    db: Session = Depends(get_db)
):
    if not verify_twilio_signature(request):
        raise HTTPException(status_code=403, detail="Invalid signature")

    phone = From.replace("whatsapp:", "")

    report = Report(
        source="whatsapp",
        raw_text=Body.strip(),
        phone=phone
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    service = ReportService(db)
    await service.trigger_ai_analysis(report)

    return {"status": "received", "report_id": str(report.id)}


@router.post("/voice")
async def receive_voice(
    request: Request,
    From: str,
    RecordingUrl: Optional[str] = None,
    TranscriptionText: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not verify_twilio_signature(request):
        raise HTTPException(status_code=403, detail="Invalid signature")

    if TranscriptionText:
        text = TranscriptionText.strip()
    elif RecordingUrl:
        text = f"Audio recording: {RecordingUrl}"
    else:
        text = "Voice report with no content"

    report = Report(
        source="voice",
        raw_text=text,
        phone=From
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    service = ReportService(db)
    await service.trigger_ai_analysis(report)

    return {"status": "received", "report_id": str(report.id)}


@router.post("/icpac")
async def receive_icpac_alert(
    request: Request,
    body: dict,
    db: Session = Depends(get_db)
):
    if not verify_icpac_signature(request, body):
        raise HTTPException(status_code=403, detail="Invalid signature")

    affected_areas = body.get("affected_areas", [])
    location = affected_areas[0] if affected_areas else {}

    from app.models import Incident

    incident = Incident(
        title=body.get("headline", "ICPAC Alert"),
        description=body.get("description", ""),
        hazard_type=body.get("alert_type", "flood"),
        severity=body.get("severity", "medium"),
        latitude=location.get("lat", 0),
        longitude=location.get("lng", 0),
        location_name=location.get("name", "Unknown")
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return {"status": "received", "internal_incident_id": str(incident.id)}