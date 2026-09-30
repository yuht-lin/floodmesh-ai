from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
import enum
from app.database import Base


class IncidentStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    PRIORITIZED = "PRIORITIZED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    original_report = Column(Text, nullable=False)
    language = Column(String, default="en")
    
    people_affected = Column(Integer, default=1)
    vulnerable_people = Column(Integer, default=0)
    medical_urgency = Column(String, default="low")
    flood_severity = Column(String, default="medium")
    isolation_level = Column(String, default="medium")
    accessibility = Column(String, default="fair")
    incident_type = Column(String, default="trapped_residents")
    source = Column(String, default="citizen_report")
    confidence = Column(Float, default=1.0)
    
    required_resource_type = Column(String, default="rescue_boat")
    required_capacity = Column(Integer, default=1)
    
    status = Column(String, default=IncidentStatus.REPORTED)
    priority_score = Column(Float, default=0.0)
    priority_level = Column(String, default="MEDIUM")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
