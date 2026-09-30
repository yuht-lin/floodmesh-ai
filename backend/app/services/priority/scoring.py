from typing import Dict, Any, Tuple, List


def calculate_priority_score(data: Dict[str, Any]) -> Tuple[float, str, List[str]]:
    reasons: List[str] = []
    score: float = 0.0

    # 1. Medical Urgency (Max 30 pts)
    medical_urgency = str(data.get("medical_urgency", "low")).lower()
    medical_map = {"critical": 30.0, "high": 22.0, "medium": 12.0, "low": 4.0}
    med_pts = medical_map.get(medical_urgency, 4.0)
    score += med_pts
    if med_pts >= 22.0:
        reasons.append(f"+ High/Critical Medical Urgency ({medical_urgency.upper()}): +{med_pts:.0f} pts")

    # 2. Vulnerable Population (Max 20 pts)
    vulnerable_count = int(data.get("vulnerable_people", 0))
    vuln_pts = min(20.0, vulnerable_count * 5.0)
    score += vuln_pts
    if vulnerable_count > 0:
        reasons.append(f"+ {vulnerable_count} Vulnerable Persons: +{vuln_pts:.0f} pts")

    # 3. People Affected (Max 20 pts)
    people_affected = int(data.get("people_affected", 1))
    pop_pts = min(20.0, people_affected * 1.2)
    score += pop_pts
    reasons.append(f"+ {people_affected} People Affected: +{pop_pts:.1f} pts")

    # 4. Flood Severity (Max 15 pts)
    severity = str(data.get("flood_severity", "medium")).lower()
    sev_map = {"severe": 15.0, "high": 12.0, "medium": 8.0, "low": 3.0}
    sev_pts = sev_map.get(severity, 8.0)
    score += sev_pts
    if sev_pts >= 12.0:
        reasons.append(f"+ Severe/High Flood Impact ({severity.upper()}): +{sev_pts:.0f} pts")

    # 5. Accessibility & Isolation (Max 15 pts)
    accessibility = str(data.get("accessibility", "fair")).lower()
    access_map = {"inaccessible": 15.0, "poor": 10.0, "fair": 5.0, "good": 0.0}
    acc_pts = access_map.get(accessibility, 5.0)
    score += acc_pts
    if acc_pts >= 10.0:
        reasons.append(f"+ Difficult Access/Isolation ({accessibility.upper()}): +{acc_pts:.0f} pts")

    final_score = round(min(100.0, score), 1)

    if final_score >= 80.0:
        level = "CRITICAL"
    elif final_score >= 60.0:
        level = "HIGH"
    elif final_score >= 40.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return final_score, level, reasons
