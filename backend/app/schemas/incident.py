from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IncidentBase(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    location_name: str
    description: str
    original_report: str
    language: str = "en"
    people_affected: int = Field(default=1, ge=1)
    vulnerable_people: int = Field(default=0, ge=0)
    medical_urgency: str = "low"
    flood_severity: str = "medium"
    isolation_level: str = "medium"
    accessibility: str = "fair"
    incident_type: str = "trapped_residents"
    source: str = "citizen_report"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    required_resource_type: str = "rescue_boat"
    required_capacity: int = Field(default=1, ge=1)


class IncidentCreate(IncidentBase):
    incident_id: Optional[str] = None


class IncidentUpdate(BaseModel):
    people_affected: Optional[int] = Field(None, ge=1)
    vulnerable_people: Optional[int] = Field(None, ge=0)
    medical_urgency: Optional[str] = None
    flood_severity: Optional[str] = None
    isolation_level: Optional[str] = None
    accessibility: Optional[str] = None
    status: Optional[str] = None
    priority_score: Optional[float] = None
    priority_level: Optional[str] = None


class ReportIngestRequest(BaseModel):
    report_text: str = Field(..., min_length=5, description="Raw distress report text")
    source: str = Field(default="social_media", description="Data source")


class IncidentResponse(IncidentBase):
    incident_id: str
    status: str
    priority_score: float
    priority_level: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
