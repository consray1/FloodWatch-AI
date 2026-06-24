from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class AlertBase(BaseModel):
    incident_id: Optional[UUID] = None
    title: str = Field(..., min_length=5, max_length=255)
    message: str = Field(..., min_length=10)
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    channel: str = Field(..., pattern="^(sms|email|whatsapp|push)$")
    target_audience: Optional[str] = Field(None, pattern="^(all|responders|admins)$")


class AlertCreate(AlertBase):
    pass


class AlertResponse(BaseModel):
    id: UUID
    incident_id: Optional[UUID]
    title: str
    severity: str
    channel: str
    status: str
    recipients_count: Optional[int] = None
    sent_at: Optional[datetime] = None
    created_by: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlertDetailResponse(AlertResponse):
    message: str
    recipients: Optional[dict] = None


class AlertListResponse(BaseModel):
    data: List[AlertResponse]
    pagination: dict