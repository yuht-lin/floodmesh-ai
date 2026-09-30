from app.services.allocation.solver import solve_resource_allocation


def test_or_tools_allocation():
    incidents = [
        {
            "incident_id": "INC-001",
            "latitude": 26.65,
            "longitude": 92.79,
            "priority_score": 90.0,
            "required_resource_type": "rescue_boat",
            "people_affected": 5,
            "medical_urgency": "high",
            "accessibility": "inaccessible"
        }
    ]
    resources = [
        {
            "resource_id": "BOAT-001",
            "resource_type": "rescue_boat",
            "latitude": 26.64,
            "longitude": 92.78,
            "capacity": 10,
            "status": "AVAILABLE",
            "medical_capability": True,
            "speed_kmh": 30.0
        },
        {
            "resource_id": "AMB-001",
            "resource_type": "ambulance",
            "latitude": 26.65,
            "longitude": 92.79,
            "capacity": 2,
            "status": "AVAILABLE",
            "medical_capability": True,
            "speed_kmh": 50.0
        }
    ]

    recommendations = solve_resource_allocation(incidents, resources)
    assert len(recommendations) == 1
    assert recommendations[0]["incident_id"] == "INC-001"
    assert recommendations[0]["resource_id"] == "BOAT-001"
