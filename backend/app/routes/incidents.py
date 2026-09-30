import uuid
import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import Incident
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/incidents", tags=["Incidents"])


class IngestReportRequest(BaseModel):
    report_text: Optional[str] = Field(None)
    raw_report_text: Optional[str] = Field(None)
    source: Optional[str] = Field("web_live_gps")
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)


def calculate_priority(extracted_data: dict, raw_text: str) -> float:
    """Calculates a dynamic emergency priority score (0-100) scaling with crowd mass and critical needs."""
    text_lower = raw_text.lower()
    
    # 1. Base Urgency Weight (Max 35)
    urgency_map = {"critical": 35, "high": 28, "medium": 18, "low": 10}
    urgency = str(extracted_data.get("medical_urgency", "medium")).lower()
    base_urgency = urgency_map.get(urgency, 20)

    # 2. Dynamic Scale for Affected People (Max 45)
    people = int(extracted_data.get("people_affected", 1))
    if people >= 100:
        people_weight = 45
    elif people >= 50:
        people_weight = 38
    elif people >= 20:
        people_weight = 30
    elif people >= 10:
        people_weight = 22
    elif people >= 5:
        people_weight = 15
    else:
        people_weight = max(people * 3, 5)

    # 3. Isolation & Critical Needs Boost (Max 20)
    isolation_map = {"high": 15, "medium": 10, "low": 5}
    isolation = str(extracted_data.get("isolation_level", "medium")).lower()
    iso_weight = isolation_map.get(isolation, 5)

    need_boost = 0
    if any(w in text_lower for w in ["medicine", "medical", "food", "trapped", "roof", "boat", "water"]):
        need_boost += 5

    total_score = float(base_urgency + people_weight + iso_weight + need_boost)
    return min(max(total_score, 10.0), 100.0)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("/ingest", status_code=status.HTTP_201_CREATED)
@router.post("/ingest-report", status_code=status.HTTP_201_CREATED)
async def ingest_report(payload: IngestReportRequest, db: Session = Depends(get_db)):
    raw_text = payload.report_text or payload.raw_report_text or "Emergency SOS Report"

    # Extract details via Gemini or Local NLP Fallback
    try:
        extracted_data = await gemini_service.extract_incident_info(raw_text)
    except Exception:
        extracted_data = {
            "people_affected": 1,
            "medical_urgency": "medium",
            "isolation_level": "medium",
        }

    lat = payload.latitude if payload.latitude is not None else extracted_data.get("latitude")
    lng = payload.longitude if payload.longitude is not None else extracted_data.get("longitude")

    if lat is None or lng is None:
        lat, lng = 26.43, 92.03

    priority = calculate_priority(extracted_data, raw_text)
    gen_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    now_dt = datetime.datetime.utcnow()

    try:
        new_incident = Incident()

        setattr(new_incident, "incident_id", gen_id)
        setattr(new_incident, "latitude", float(lat))
        setattr(new_incident, "longitude", float(lng))
        setattr(new_incident, "location_name", f"Live GPS ({lat:.4f}, {lng:.4f})")
        setattr(new_incident, "description", raw_text)
        setattr(new_incident, "original_report", raw_text)

        for attr, val in [
            ("timestamp", now_dt),
            ("language", "en"),
            ("people_affected", int(extracted_data.get("people_affected", 1))),
            ("vulnerable_people", 0),
            ("medical_urgency", str(extracted_data.get("medical_urgency", "medium"))),
            ("flood_severity", "high" if priority >= 70 else "medium"),
            ("isolation_level", str(extracted_data.get("isolation_level", "medium"))),
            ("accessibility", "fair"),
            ("incident_type", "trapped_residents"),
            ("source", payload.source or "web_live_gps"),
            ("confidence", 1.0),
            ("required_resource_type", "rescue_boat"),
            ("required_capacity", 1),
            ("status", "pending"),
            ("priority_score", priority),
            ("priority_level", "CRITICAL" if priority >= 80 else ("HIGH" if priority >= 60 else "MEDIUM")),
            ("created_at", now_dt),
            ("updated_at", now_dt),
        ]:
            if hasattr(new_incident, attr):
                setattr(new_incident, attr, val)

        db.add(new_incident)
        db.commit()
        db.refresh(new_incident)

        return {
            "status": "success",
            "message": "Incident ingested successfully",
            "incident": {
                "id": gen_id,
                "raw_report_text": raw_text,
                "priority_score": priority,
                "latitude": float(lat),
                "longitude": float(lng),
                "status": "pending",
            },
        }
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Ingestion Error: {str(err)}",
        )


@router.get("")
@router.get("/")
async def get_incidents(db: Session = Depends(get_db)):
    """Return incidents ordered by highest priority score first."""
    incidents = db.query(Incident).order_by(Incident.priority_score.desc()).all()
    output = []
    for inc in incidents:
        inc_id = getattr(inc, "incident_id", None) or getattr(inc, "id", None) or "INC-000"
        report_text = getattr(inc, "raw_report_text", None) or getattr(inc, "description", None) or "Emergency Report"
        output.append({
            "id": str(inc_id),
            "incident_id": str(inc_id),
            "raw_report_text": str(report_text),
            "description": str(report_text),
            "priority_score": float(getattr(inc, "priority_score", 40.0) or 40.0),
            "people_affected": int(getattr(inc, "people_affected", 1) or 1),
            "medical_urgency": str(getattr(inc, "medical_urgency", "medium") or "medium"),
            "latitude": float(inc.latitude),
            "longitude": float(inc.longitude),
            "status": str(getattr(inc, "status", "pending") or "pending"),
        })
    return output
