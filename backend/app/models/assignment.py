from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text
from app.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, nullable=False, index=True)
    resource_id = Column(String, nullable=False, index=True)
    
    estimated_travel_time_mins = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    recommendation_score = Column(Float, default=0.0)
    recommendation_reason = Column(Text, nullable=False)
    
    approval_status = Column(String, default="PENDING")
    rejection_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
