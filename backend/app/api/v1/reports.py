from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.models import Report, User, ReportMedia, AIAnalysis
from app.schemas import ReportCreate, ReportUpdate, ReportResponse, ReportListResponse, LocationResponse
from app.api.v1.deps import get_current_user, require_responder, require_analyst
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


def build_report_response(report: Report) -> ReportResponse:
    location = LocationResponse(
        lat=float(report.location_lat) if report.location_lat else None,
        lng=float(report.location_lng) if report.location_lng else None,
        name=report.location_name
    )

    media = []
    for m in report.media:
        media.append({
            "id": m.id,
            "url": m.media_url,
            "type": m.media_type
        })

    reporter = None
    if report.reporter:
        reporter = {
            "id": report.reporter.id,
            "name": report.reporter.name,
            "trust_score": report.reporter.trust_score.score if report.reporter.trust_score else None
        }

    ai_analysis = None
    if report.ai_analysis:
        ai_analysis = {
            "id": report.ai_analysis.id,
            "hazard_type": report.ai_analysis.hazard_type,
            "severity": report.ai_analysis.severity,
            "confidence": float(report.ai_analysis.confidence) if report.ai_analysis.confidence else None
        }

    incident = None
    if report.incident_reports:
        ir = report.incident_reports[0]
        incident = {
            "id": ir.incident.id,
            "title": ir.incident.title,
            "severity": ir.incident.severity
        }

    return ReportResponse(
        id=report.id,
        source=report.source,
        status=report.status,
        raw_text=report.raw_text,
        location=location,
        media=media,
        reporter=reporter,
        ai_analysis=ai_analysis,
        incident=incident,
        created_at=report.created_at
    )


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    report = Report(
        source=report_data.source,
        reporter_id=current_user.id if current_user else None,
        raw_text=report_data.raw_text,
        location_lat=report_data.location_lat,
        location_lng=report_data.location_lng,
        location_name=report_data.location_name
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    service = ReportService(db)
    await service.trigger_ai_analysis(report)

    return build_report_response(report)


@router.get("", response_model=ReportListResponse)
async def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    source: Optional[str] = None,
    status: Optional[str] = None,
    hazard_type: Optional[str] = None,
    reporter_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Report).options(
        joinedload(Report.reporter).joinedload(User.trust_score),
        joinedload(Report.media),
        joinedload(Report.ai_analysis),
        joinedload(Report.incident_reports).joinedload(Report.incident_reports)
    )

    if source:
        query = query.filter(Report.source == source)
    if status:
        query = query.filter(Report.status == status)
    if reporter_id:
        query = query.filter(Report.reporter_id == reporter_id)

    total = query.count()
    reports = query.order_by(Report.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return ReportListResponse(
        data=[build_report_response(r) for r in reports],
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).options(
        joinedload(Report.reporter).joinedload(User.trust_score),
        joinedload(Report.media),
        joinedload(Report.ai_analysis),
        joinedload(Report.incident_reports).joinedload(Report.incident_reports)
    ).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return build_report_response(report)


@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: UUID,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.reporter_id != current_user.id and current_user.role.name not in ["admin", "responder"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if report_data.raw_text is not None:
        report.raw_text = report_data.raw_text
    if report_data.location_lat is not None:
        report.location_lat = report_data.location_lat
    if report_data.location_lng is not None:
        report.location_lng = report_data.location_lng
    if report_data.location_name is not None:
        report.location_name = report_data.location_name

    db.commit()
    db.refresh(report)

    return build_report_response(report)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.reporter_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(report)
    db.commit()