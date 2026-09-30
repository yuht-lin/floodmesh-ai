import os
import json
import logging
from typing import Dict, Any
from pydantic import BaseModel, Field
from app.config import settings

logger = logging.getLogger(__name__)


class ExtractedIncidentSchema(BaseModel):
    location_name: str = Field(description="Extracted location, landmark, or village name")
    latitude: float = Field(default=26.6528, description="Estimated latitude coordinate")
    longitude: float = Field(default=92.7926, description="Estimated longitude coordinate")
    description: str = Field(description="English summary and translation of the distress report")
    language: str = Field(default="en", description="Detected language code (e.g., as, hi, bn, en)")
    people_affected: int = Field(default=1, description="Number of people stranded or affected")
    vulnerable_people: int = Field(default=0, description="Number of elderly, children, pregnant, or sick persons")
    medical_urgency: str = Field(default="low", description="Medical urgency: low, medium, high, or critical")
    flood_severity: str = Field(default="medium", description="Flood severity: low, medium, high, or severe")
    isolation_level: str = Field(default="medium", description="Isolation level: low, medium, or high")
    accessibility: str = Field(default="fair", description="Accessibility: good, fair, poor, or inaccessible")
    incident_type: str = Field(default="trapped_residents", description="trapped_residents, medical_emergency, evacuation_request, stranded_vehicle, shelter_request")
    required_resource_type: str = Field(default="rescue_boat", description="rescue_boat, ambulance, relief_vehicle, rescue_team")
    required_capacity: int = Field(default=1, description="Minimum capacity required")
    confidence: float = Field(default=0.9, description="Extraction confidence score 0.0 - 1.0")


def fallback_extractor(raw_report: str) -> Dict[str, Any]:
    text_lower = raw_report.lower()
    
    medical_urgency = "low"
    if any(w in text_lower for w in ["pregnant", "hospital", "patient", "sick", "injured", "medical", "বেমাৰ", "अस्पताल", "রোগী"]):
        medical_urgency = "critical" if any(w in text_lower for w in ["pregnant", "hospital"]) else "high"
        
    people_affected = 5
    import re
    numbers = [int(s) for s in re.findall(r'\d+', raw_report)]
    if numbers:
        people_affected = max(numbers[0], 1)
        
    vulnerable_people = 1 if medical_urgency in ["high", "critical"] else 0
    
    req_resource = "rescue_boat"
    if medical_urgency == "critical" and "ambulance" in text_lower:
        req_resource = "ambulance"
    elif any(w in text_lower for w in ["school", "food", "water", "খাবার"]):
        req_resource = "relief_vehicle"
        
    return {
        "location_name": "Sonitpur District Flood Zone",
        "latitude": 26.6528,
        "longitude": 92.7926,
        "description": f"Processed distress report: {raw_report[:120]}",
        "language": "auto",
        "people_affected": people_affected,
        "vulnerable_people": vulnerable_people,
        "medical_urgency": medical_urgency,
        "flood_severity": "high",
        "isolation_level": "high",
        "accessibility": "poor",
        "incident_type": "trapped_residents",
        "required_resource_type": req_resource,
        "required_capacity": people_affected,
        "confidence": 0.85
    }


def extract_incident_from_report(raw_report: str) -> Dict[str, Any]:
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        logger.warning("GEMINI_API_KEY not set. Using rule-based fallback extractor.")
        return fallback_extractor(raw_report)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are an expert emergency NLP extraction agent for flood disaster response in India. "
            "Analyze the raw distress report (Assamese, Hindi, Bengali, or English) "
            "and extract structured disaster response parameters in JSON matching the schema."
        )

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=f"Extract structured emergency incident parameters from this distress report:\n\n{raw_report}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ExtractedIncidentSchema,
                temperature=0.1
            )
        )
        
        return json.loads(response.text)

    except Exception as e:
        logger.error(f"Gemini API extraction failed: {e}. Falling back to rule engine.")
        return fallback_extractor(raw_report)
