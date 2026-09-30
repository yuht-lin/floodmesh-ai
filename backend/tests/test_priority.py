from app.services.priority.scoring import calculate_priority_score


def test_critical_medical_priority():
    data = {
        "medical_urgency": "critical",
        "vulnerable_people": 3,
        "people_affected": 15,
        "flood_severity": "severe",
        "accessibility": "inaccessible"
    }
    score, level, reasons = calculate_priority_score(data)
    assert score >= 80.0
    assert level == "CRITICAL"
    assert any("Critical Medical Urgency" in r for r in reasons)


def test_low_priority_incident():
    data = {
        "medical_urgency": "low",
        "vulnerable_people": 0,
        "people_affected": 1,
        "flood_severity": "low",
        "accessibility": "good"
    }
    score, level, reasons = calculate_priority_score(data)
    assert score < 40.0
    assert level == "LOW"
