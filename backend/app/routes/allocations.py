import math
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ortools.linear_solver import pywraplp

from app.database import get_db
from app.models.incident import Incident
from app.models.resource import Resource

router = APIRouter(prefix="/allocations", tags=["Allocations"])


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@router.post("/recalculate")
async def recalculate_allocations(db: Session = Depends(get_db)):
    incidents = (
        db.query(Incident)
        .filter(Incident.status == "pending")
        .order_by(Incident.priority_score.desc())
        .all()
    )
    resources = db.query(Resource).filter(Resource.status == "available").all()

    if not incidents:
        return {"status": "success", "message": "No pending incidents.", "assignments": [], "unassigned_queue": []}

    num_incidents = len(incidents)
    num_resources = len(resources)

    solver = pywraplp.Solver.CreateSolver("SCIP") or pywraplp.Solver.CreateSolver("CBC")
    
    x = {}
    for i in range(num_incidents):
        for j in range(num_resources):
            x[i, j] = solver.BoolVar(f"x_{i}_{j}")

    for i in range(num_incidents):
        solver.Add(solver.Sum([x[i, j] for j in range(num_resources)]) <= 1)

    for j in range(num_resources):
        solver.Add(solver.Sum([x[i, j] for i in range(num_incidents)]) <= 1)

    objective_terms = []
    dist_matrix = []

    for i, inc in enumerate(incidents):
        p_score = float(getattr(inc, "priority_score", 40.0))
        inc_lat, inc_lng = float(inc.latitude), float(inc.longitude)

        row_dist = []
        for j, res in enumerate(resources):
            res_lat, res_lng = float(res.latitude), float(res.longitude)
            dist = haversine_distance(inc_lat, inc_lng, res_lat, res_lng)
            row_dist.append(dist)

            efficiency = (p_score ** 2) / (dist + 0.5)
            objective_terms.append(x[i, j] * efficiency)

        dist_matrix.append(row_dist)

    solver.Maximize(solver.Sum(objective_terms))
    solver_status = solver.Solve()

    assignments = []
    assigned_incident_ids = set()

    if solver_status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        for i, inc in enumerate(incidents):
            for j, res in enumerate(resources):
                if x[i, j].solution_value() > 0.5:
                    inc_id = getattr(inc, "incident_id", getattr(inc, "id", "INC-000"))
                    res_id = getattr(res, "resource_id", getattr(res, "id", "RES-000"))
                    dist_km = round(dist_matrix[i][j], 2)
                    eta_mins = max(1, round((dist_km / 30.0) * 60))

                    assignments.append({
                        "incident_id": inc_id,
                        "incident_text": getattr(inc, "raw_report_text", getattr(inc, "description", "SOS")),
                        "priority_score": float(getattr(inc, "priority_score", 40.0)),
                        "incident_lat": float(inc.latitude),
                        "incident_lng": float(inc.longitude),
                        "resource_id": res_id,
                        "resource_name": getattr(res, "name", f"Resource #{res_id}"),
                        "resource_type": getattr(res, "resource_type", getattr(res, "type", "rescue_boat")),
                        "resource_lat": float(res.latitude),
                        "resource_lng": float(res.longitude),
                        "distance_km": dist_km,
                        "eta_minutes": eta_mins,
                        "match_reason": f"Priority Proximity Match | Score: {getattr(inc, 'priority_score', 40)}/100 | Dist: {dist_km} km",
                        "status": "assigned",
                    })
                    assigned_incident_ids.add(inc_id)

    # Build queue of remaining unassigned reports priority wise
    unassigned_queue = []
    for inc in incidents:
        inc_id = getattr(inc, "incident_id", getattr(inc, "id", "INC-000"))
        if inc_id not in assigned_incident_ids:
            unassigned_queue.append({
                "incident_id": inc_id,
                "incident_text": getattr(inc, "raw_report_text", getattr(inc, "description", "SOS")),
                "priority_score": float(getattr(inc, "priority_score", 40.0)),
                "latitude": float(inc.latitude),
                "longitude": float(inc.longitude),
                "status": "pending_resource",
            })

    return {
        "status": "success",
        "message": f"OR-Tools solver completed. {len(assignments)} assigned, {len(unassigned_queue)} unassigned.",
        "assignments": assignments,
        "unassigned_queue": unassigned_queue,
    }


@router.get("")
@router.get("/")
async def get_allocations(db: Session = Depends(get_db)):
    return await recalculate_allocations(db)
