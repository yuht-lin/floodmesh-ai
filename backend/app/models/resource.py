from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from app.database import Base


class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(String, primary_key=True, index=True)
    resource_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity = Column(Integer, default=1)
    
    status = Column(String, default="AVAILABLE")
    medical_capability = Column(Boolean, default=False)
    team_size = Column(Integer, default=2)
    speed_kmh = Column(Float, default=25.0)
    
    current_assignment_id = Column(String, nullable=True)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
