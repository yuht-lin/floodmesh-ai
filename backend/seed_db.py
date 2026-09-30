from app.database import engine, Base, SessionLocal
from app.models.incident import Incident
from app.models.resource import Resource
from app.models.assignment import Assignment
from app.models.audit import AuditLog

def init_and_seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    db.query(Assignment).delete()
    db.query(Incident).delete()
    db.query(Resource).delete()
    db.query(AuditLog).delete()
    db.commit()

    incidents = [
        Incident(
            incident_id="INC-ASSAM-001",
            latitude=26.6528,
            longitude=92.7926,
            location_name="Tezpur Rubber Garden",
            description="15 people stranded on roofs due to sudden flash flood.",
            original_report="মানুহ ১৫ জন চালত আৱদ্ধ হৈ আছে।",
            language="as",
            people_affected=15,
            vulnerable_people=3,
            medical_urgency="high",
            flood_severity="high",
            isolation_level="high",
            accessibility="poor",
            incident_type="trapped_residents",
            source="hotline",
            required_resource_type="rescue_boat",
            required_capacity=15,
            status="REPORTED",
            priority_score=85.0,
            priority_level="CRITICAL"
        ),
        Incident(
            incident_id="INC-ASSAM-002",
            latitude=26.7120,
            longitude=92.8310,
            location_name="Dhekiajuli Primary Health Center",
            description="Pregnant woman needs immediate evacuation to civil hospital.",
            original_report="एक गर्भवती महिला को तुरंत अस्पताल ले जाना है।",
            language="hi",
            people_affected=2,
            vulnerable_people=1,
            medical_urgency="critical",
            flood_severity="medium",
            isolation_level="medium",
            accessibility="fair",
            incident_type="medical_emergency",
            source="citizen_report",
            required_resource_type="ambulance",
            required_capacity=2,
            status="REPORTED",
            priority_score=59.4,
            priority_level="MEDIUM"
        ),
        Incident(
            incident_id="INC-ASSAM-003",
            latitude=26.8011,
            longitude=92.8622,
            location_name="Jamugurihat Relief Camp",
            description="Clean water and food ration needed for 100 flood victims.",
            original_report="Relief supplies needed at Jamugurihat school.",
            language="en",
            people_affected=100,
            vulnerable_people=25,
            medical_urgency="low",
            flood_severity="high",
            isolation_level="high",
            accessibility="poor",
            incident_type="shelter_request",
            source="social_media",
            required_resource_type="relief_vehicle",
            required_capacity=100,
            status="REPORTED",
            priority_score=69.0,
            priority_level="HIGH"
        )
    ]
    db.add_all(incidents)

    resources = [
        Resource(
            resource_id="NDRF-BOAT-01",
            resource_type="rescue_boat",
            name="NDRF Motorized Boat 01",
            latitude=26.6400,
            longitude=92.7800,
            capacity=12,
            status="AVAILABLE",
            medical_capability=False,
            team_size=4,
            speed_kmh=20.0
        ),
        Resource(
            resource_id="NDRF-BOAT-02",
            resource_type="rescue_boat",
            name="NDRF Heavy Boat 02",
            latitude=26.7500,
            longitude=93.1000,
            capacity=20,
            status="AVAILABLE",
            medical_capability=False,
            team_size=6,
            speed_kmh=18.0
        ),
        Resource(
            resource_id="AMB-SONITPUR-101",
            resource_type="ambulance",
            name="108 Emergency Ambulance 101",
            latitude=26.7000,
            longitude=92.8100,
            capacity=2,
            status="AVAILABLE",
            medical_capability=True,
            team_size=2,
            speed_kmh=50.0
        ),
        Resource(
            resource_id="RELIEF-TRUCK-01",
            resource_type="relief_vehicle",
            name="Assam SDMA Relief Truck 01",
            latitude=26.7500,
            longitude=92.8000,
            capacity=200,
            status="AVAILABLE",
            medical_capability=False,
            team_size=3,
            speed_kmh=40.0
        )
    ]
    db.add_all(resources)

    db.commit()
    print("Database populated successfully in floodmesh.db!")
    db.close()

if __name__ == "__main__":
    init_and_seed_db()
