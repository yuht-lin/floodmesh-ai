from app.services.ai.gemini_extractor import extract_incident_from_report


def test_gemini_extraction_structure():
    raw_text = "মানুহ ১৫ জন চালত আৱদ্ধ হৈ আছে। দুজন বৃদ্ধ লোক বেমাৰত পৰিছে, সোনকালে নাও পঠিয়াওক।"
    result = extract_incident_from_report(raw_text)
    
    assert "people_affected" in result
    assert "medical_urgency" in result
    assert "required_resource_type" in result
    assert result["people_affected"] >= 1
