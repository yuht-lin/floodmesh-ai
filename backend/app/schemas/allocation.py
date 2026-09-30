from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class AssignmentResponse(BaseModel):
    assignment_id: str
    incident_id: str
    resource_id: str
    estimated_travel_time_mins: float
    distance_km: float
    recommendation_score: float
    recommendation_reason: str
    approval_status: str
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecalculateRequest(BaseModel):
    incident_ids: Optional[List[str]] = None
    force_reallocate: bool = False


class ApprovalPayload(BaseModel):
    responder_notes: Optional[str] = None


class RejectionPayload(BaseModel):
    reason: str = Field(..., min_length=3)


class ModificationPayload(BaseModel):
    new_resource_id: str
    reason: str = Field(..., min_length=3)
