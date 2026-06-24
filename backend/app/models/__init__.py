import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), default=None)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    reports = relationship("Report", back_populates="reporter")
    trust_score = relationship("TrustScore", back_populates="user", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="actor")


class TrustScore(Base):
    __tablename__ = "trust_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    score = Column(Integer, nullable=False)
    factors = Column(JSONB)
    reason = Column(Text)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="trust_score", foreign_keys=[user_id])

    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="chk_trust_score"),
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(20), nullable=False)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    raw_text = Column(Text, nullable=False)
    location_lat = Column(Numeric(10, 8))
    location_lng = Column(Numeric(11, 8))
    location_name = Column(String(255))
    status = Column(String(20), default="pending")
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reporter = relationship("User", back_populates="reports")
    media = relationship("ReportMedia", back_populates="report")
    ai_analysis = relationship("AIAnalysis", back_populates="report", uselist=False)
    incident_reports = relationship("IncidentReport", back_populates="report")

    __table_args__ = (
        CheckConstraint("source IN ('web', 'sms', 'whatsapp', 'voice', 'icpac')", name="chk_report_source"),
        CheckConstraint("status IN ('pending', 'analyzed', 'verified', 'dismissed')", name="chk_report_status"),
    )


class ReportMedia(Base):
    __tablename__ = "report_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    media_url = Column(String(500), nullable=False)
    media_type = Column(String(20), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="media")

    __table_args__ = (
        CheckConstraint("media_type IN ('image', 'video', 'audio')", name="chk_media_type"),
    )


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), unique=True, nullable=False)
    hazard_type = Column(String(50))
    hazard_category = Column(String(50))
    severity = Column(String(10))
    confidence = Column(Numeric(5, 4))
    entities = Column(JSONB)
    summary = Column(Text)
    model_version = Column(String(20), nullable=False)
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="ai_analysis")

    __table_args__ = (
        CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name="chk_ai_severity"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="chk_confidence"),
    )


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    hazard_type = Column(String(50), nullable=False)
    severity = Column(String(10), nullable=False)
    status = Column(String(20), default="active")
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    location_name = Column(String(255))
    affected_radius_km = Column(Numeric(10, 2))
    reporter_count = Column(Integer, default=1)
    verified = Column(Boolean, default=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)

    incident_reports = relationship("IncidentReport", back_populates="incident")
    risk_scores = relationship("RiskScore", back_populates="incident")
    alerts = relationship("Alert", back_populates="incident")

    __table_args__ = (
        CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name="chk_incident_severity"),
        CheckConstraint("status IN ('active', 'contained', 'resolved', 'closed')", name="chk_incident_status"),
    )


class IncidentReport(Base):
    __tablename__ = "incident_reports"

    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), primary_key=True)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), primary_key=True)
    confidence_score = Column(Numeric(5, 4))
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="incident_reports")
    report = relationship("Report", back_populates="incident_reports")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(10), nullable=False)
    channel = Column(String(20), nullable=False)
    target_audience = Column(String(50))
    recipients = Column(JSONB)
    status = Column(String(20), default="pending")
    sent_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="alerts")

    __table_args__ = (
        CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name="chk_alert_severity"),
        CheckConstraint("channel IN ('sms', 'email', 'whatsapp', 'push')", name="chk_alert_channel"),
        CheckConstraint("status IN ('pending', 'sent', 'failed')", name="chk_alert_status"),
    )


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    factors = Column(JSONB)
    model_version = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="risk_scores")


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    address = Column(String(500))
    capacity = Column(Integer, nullable=False)
    occupancy = Column(Integer, default=0)
    status = Column(String(20), default="available")
    facilities = Column(JSONB)
    contact_phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("capacity > 0", name="chk_shelter_capacity"),
        CheckConstraint("occupancy >= 0 AND occupancy <= capacity", name="chk_shelter_occupancy"),
    )


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    address = Column(String(500))
    phone = Column(String(20))
    emergency_phone = Column(String(20))
    beds_total = Column(Integer)
    beds_available = Column(Integer)
    status = Column(String(20), default="open")
    services = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    actor_ip = Column(String(45))
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(UUID(as_uuid=True))
    details = Column(JSONB)
    status = Column(String(20))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    actor = relationship("User", back_populates="audit_logs")