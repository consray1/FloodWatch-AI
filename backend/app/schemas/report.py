from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import re


class ReportBase(BaseModel):
    source: str = Field(..., description="web, sms, whatsapp, voice, icpac")
    raw_text: str = Field(..., min_length=10, max_length=5000)
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=255)

    @validator("raw_text")
    def sanitize_text(cls, v):
        v = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", v)
        return v.strip()


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    raw_text: Optional[str] = Field(None, min_length=10, max_length=5000)
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=255)


class MediaResponse(BaseModel):
    id: UUID
    url: str
    type: str

    class Config:
        from_attributes = True


class ReporterResponse(BaseModel):
    id: UUID
    name: str
    trust_score: Optional[int] = None


class AIAnalysisResponse(BaseModel):
    id: UUID
    hazard_type: Optional[str] = None
    severity: Optional[str] = None
    confidence: Optional[float] = None

    class Config:
        from_attributes = True


class LocationResponse(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    name: Optional[str] = None


class ReportResponse(BaseModel):
    id: UUID
    source: str
    status: str
    raw_text: str
    location: LocationResponse
    media: List[MediaResponse] = []
    reporter: Optional[ReporterResponse] = None
    ai_analysis: Optional[AIAnalysisResponse] = None
    incident: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    data: List[ReportResponse]
    pagination: dict