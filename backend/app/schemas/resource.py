from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ResourceBase(BaseModel):
    resource_type: str
    name: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    capacity: int = Field(default=1, ge=1)
    status: str = "AVAILABLE"
    medical_capability: bool = False
    team_size: int = Field(default=2, ge=1)
    speed_kmh: float = Field(default=25.0, gt=0.0)


class ResourceCreate(ResourceBase):
    resource_id: Optional[str] = None


class ResourceUpdate(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    status: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)
    current_assignment_id: Optional[str] = None


class ResourceResponse(ResourceBase):
    resource_id: str
    current_assignment_id: Optional[str] = None
    last_updated: datetime

    class Config:
        from_attributes = True
