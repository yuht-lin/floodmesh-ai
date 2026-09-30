import sys
import os

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal, engine, Base
from app.models import Incident, Resource, IncidentStatus, AuditLog

# Create all database tables explicitly
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    
    # Clear existing records
    db.query(Incident).delete()
    db.query(Resource).delete()
    db.query(AuditLog).delete()
    db.commit()

    sample_incidents = [
        {
            "incident_id": "INC-ASSAM-001",
            "latitude": 26.6528,
            "longitude": 92.7926,
            "location_name": "Tezpur Riverside, Sonitpur",
            "description": "15 residents trapped on rooftops due to sudden Brahmaputra river overflow. Two elderly citizens need immediate medical attention.",
            "original_report": "মানুহ ১৫ জন চালত আৱদ্ধ হৈ আছে। দুজন বৃদ্ধ লোক বেমাৰত পৰিছে, সোনকালে নাও পঠিয়াওক।",
            "language": "as",
            "people_affected": 15,
            "vulnerable_people": 3,
            "medical_urgency": "high",
            "flood_severity": "severe",
            "isolation_level": "high",
            "accessibility": "inaccessible",
            "incident_type": "trapped_residents",
            "required_resource_type": "rescue_boat",
            "required_capacity": 15,
            "status": IncidentStatus.REPORTED.value,
            "priority_score": 92.5,
            "priority_level": "CRITICAL"
        },
        {
            "incident_id": "INC-ASSAM-002",
            "latitude": 26.8500,
            "longitude": 92.8333,
            "location_name": "Jamugurihat Village, Sonitpur",
            "description": "Pregnant woman in labor needs urgent transport to district hospital. Road bridge washed away.",
            "original_report": "एक गर्भवती महिला को तुरंत अस्पताल ले जाना है, पुल बह गया है। एम्बुलेंस या मेडिकल बोट चाहिए।",
            "language": "hi",
            "people_affected": 2,
            "vulnerable_people": 1,
            "medical_urgency": "critical",
            "flood_severity": "high",
            "isolation_level": "high",
            "accessibility": "poor",
            "incident_type": "medical_emergency",
            "required_resource_type": "ambulance",
            "required_capacity": 2,
            "status": IncidentStatus.REPORTED.value,
            "priority_score": 96.0,
            "priority_level": "CRITICAL"
        },
        {
            "incident_id": "INC-ASSAM-003",
            "latitude": 26.9167,
            "longitude": 93.1833,
            "location_name": "Biswanath Chariali Sector 4",
            "description": "School building surrounded by water with 25 students inside. Drinking water exhausted.",
            "original_report": "স্কুলে ২৫ জন ছাত্র আটকে আছে। খাবার ও পানীয় জল প্রয়োজন।",
            "language": "bn",
            "people_affected": 25,
            "vulnerable_people": 25,
            "medical_urgency": "medium",
            "flood_severity": "high",
            "isolation_level": "medium",
            "accessibility": "fair",
            "incident_type": "evacuation_request",
            "required_resource_type": "relief_vehicle",
            "required_capacity": 25,
            "status": IncidentStatus.REPORTED.value,
            "priority_score": 85.0,
            "priority_level": "HIGH"
        },
        {
            "incident_id": "INC-ASSAM-004",
            "latitude": 26.1445,
            "longitude": 91.7362,
            "location_name": "Zoo Road, Guwahati",
            "description": "Stranded commuter vehicle in flash flood with 3 passengers.",
            "original_report": "Car engine stalled in 4ft water on Zoo road. 3 occupants inside safely on roof.",
            "language": "en",
            "people_affected": 3,
            "vulnerable_people": 0,
            "medical_urgency": "low",
            "flood_severity": "medium",
            "isolation_level": "low",
            "accessibility": "fair",
            "incident_type": "stranded_vehicle",
            "required_resource_type": "rescue_team",
            "required_capacity": 3,
            "status": IncidentStatus.REPORTED.value,
            "priority_score": 45.0,
            "priority_level": "MEDIUM"
        },
        {
            "incident_id": "INC-ASSAM-005",
            "latitude": 26.9500,
            "longitude": 94.1667,
            "location_name": "Kamalabari, Majuli Island",
            "description": "Embankment breach near relief shelter. 40 displaced villagers requiring relocation.",
            "original_report": "মাজুলীৰ মঠাউৰি ভাঙিছে। ৪০ জন লোকক সুৰক্ষিত স্থানলৈ নিব লাগে।",
            "language": "as",
            "people_affected": 40,
            "vulnerable_people": 10,
            "medical_urgency": "medium",
            "flood_severity": "severe",
            "isolation_level": "high",
            "accessibility": "inaccessible",
            "incident_type": "shelter_request",
            "required_resource_type": "rescue_boat",
            "required_capacity": 40,
            "status": IncidentStatus.REPORTED.value,
            "priority_score": 88.0,
            "priority_level": "HIGH"
        }
    ]

    sample_resources = [
        {
            "resource_id": "NDRF-BOAT-01",
            "resource_type": "rescue_boat",
            "name": "NDRF Inflatable Motor Boat #1",
            "latitude": 26.6300,
            "longitude": 92.8000,
            "capacity": 12,
            "status": "AVAILABLE",
            "medical_capability": True,
            "team_size": 4,
            "speed_kmh": 30.0
        },
        {
            "resource_id": "NDRF-BOAT-02",
            "resource_type": "rescue_boat",
            "name": "SDRF High-Capacity Rescue Craft #2",
            "latitude": 26.8800,
            "longitude": 93.1500,
            "capacity": 20,
            "status": "AVAILABLE",
            "medical_capability": False,
            "team_size": 5,
            "speed_kmh": 25.0
        },
        {
            "resource_id": "AMB-SONITPUR-101",
            "resource_type": "ambulance",
            "name": "108 ALS Emergency Ambulance Sonitpur",
            "latitude": 26.8300,
            "longitude": 92.8200,
            "capacity": 2,
            "status": "AVAILABLE",
            "medical_capability": True,
            "team_size": 3,
            "speed_kmh": 50.0
        },
        {
            "resource_id": "RELIEF-TRUCK-01",
            "resource_type": "relief_vehicle",
            "name": "Assam State Disaster Mgmt Food/Water Truck",
            "latitude": 26.9000,
            "longitude": 93.1000,
            "capacity": 50,
            "status": "AVAILABLE",
            "medical_capability": False,
            "team_size": 2,
            "speed_kmh": 40.0
        },
        {
            "resource_id": "QUICK-RESPONSE-01",
            "resource_type": "rescue_team",
            "name": "Civil Defence Quick Response Team 1",
            "latitude": 26.1500,
            "longitude": 91.7400,
            "capacity": 6,
            "status": "AVAILABLE",
            "medical_capability": False,
            "team_size": 6,
            "speed_kmh": 45.0
        }
    ]

    for item in sample_incidents:
        inc = Incident(**item)
        db.add(inc)

    for item in sample_resources:
        res = Resource(**item)
        db.add(res)

    db.commit()
    print(f"SUCCESS: Database seeded with {len(sample_incidents)} incidents and {len(sample_resources)} resources!")
    db.close()

if __name__ == "__main__":
    seed()
