from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class IncidentBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None
    hazard_type: str = Field(..., min_length=2, max_length=50)
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_name: Optional[str] = None
    affected_radius_km: Optional[float] = Field(None, ge=0)


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = None
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    status: Optional[str] = Field(None, pattern="^(active|contained|resolved|closed)$")
    verified: Optional[bool] = None


class IncidentLocation(BaseModel):
    lat: float
    lng: float
    name: Optional[str] = None


class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    hazard_type: str
    severity: str
    status: str
    location: IncidentLocation
    affected_radius_km: Optional[float]
    reporter_count: int
    verified: bool
    risk_score: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IncidentDetailResponse(IncidentResponse):
    reports: List[dict]
    alerts: List[dict]
    nearby_shelters: List[dict]
    nearby_hospitals: List[dict]
    verified_by: Optional[dict] = None


class IncidentListResponse(BaseModel):
    data: List[IncidentResponse]
    pagination: dict