from typing import List, Dict, Any
from ortools.linear_solver import pywraplp
from app.services.routing.matrix import haversine_distance_km, calculate_travel_time_mins


def solve_resource_allocation(
    incidents: List[Dict[str, Any]],
    resources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    if not incidents or not resources:
        return []

    available_resources = [r for r in resources if r.get("status") == "AVAILABLE"]
    if not available_resources:
        return []

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return []

    x = {}
    travel_data = {}

    for i, inc in enumerate(incidents):
        inc_id = inc["incident_id"]
        priority_score = float(inc.get("priority_score", 50.0))
        req_type = inc.get("required_resource_type", "rescue_boat")
        req_med = inc.get("medical_urgency") in ["high", "critical"]

        for r, res in enumerate(available_resources):
            res_id = res["resource_id"]
            
            dist_km = haversine_distance_km(
                res["latitude"], res["longitude"],
                inc["latitude"], inc["longitude"]
            )
            travel_mins = calculate_travel_time_mins(
                dist_km,
                res.get("speed_kmh", 25.0),
                inc.get("accessibility", "fair")
            )
            
            travel_data[(inc_id, res_id)] = {
                "distance_km": dist_km,
                "travel_time_mins": travel_mins
            }

            x[i, r] = solver.BoolVar(f"x_{i}_{r}")

            type_match = (res.get("resource_type") == req_type)
            med_match = res.get("medical_capability", False) if req_med else True
            
            compatibility_bonus = 50.0 if type_match else -100.0
            medical_bonus = 30.0 if (req_med and med_match) else 0.0

            coeff = (priority_score * 2.0) - (travel_mins * 0.5) + compatibility_bonus + medical_bonus
            solver.Objective().SetCoefficient(x[i, r], coeff)

    solver.Objective().SetMaximization()

    for r in range(len(available_resources)):
        solver.Add(solver.Sum([x[i, r] for i in range(len(incidents))]) <= 1)

    for i in range(len(incidents)):
        solver.Add(solver.Sum([x[i, r] for r in range(len(available_resources))]) <= 1)

    solver_status = solver.Solve()

    recommendations = []
    if solver_status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        for i, inc in enumerate(incidents):
            inc_id = inc["incident_id"]
            for r, res in enumerate(available_resources):
                res_id = res["resource_id"]
                if x[i, r].solution_value() > 0.5:
                    t_info = travel_data[(inc_id, res_id)]
                    type_match = (res.get("resource_type") == inc.get("required_resource_type"))
                    
                    reason_parts = [
                        f"Priority Match ({inc.get('priority_score', 0):.0f} pts)",
                        f"ETA: {t_info['travel_time_mins']} mins ({t_info['distance_km']} km)"
                    ]
                    if type_match:
                        reason_parts.append(f"Exact Type Match ({res.get('resource_type')})")
                    if res.get("capacity", 1) < inc.get("people_affected", 1):
                        reason_parts.append(f"Partial Capacity Cover ({res.get('capacity')}/{inc.get('people_affected')} people)")

                    recommendations.append({
                        "incident_id": inc_id,
                        "resource_id": res_id,
                        "distance_km": t_info["distance_km"],
                        "estimated_travel_time_mins": t_info["travel_time_mins"],
                        "recommendation_score": round(solver.Objective().Value(), 1),
                        "recommendation_reason": " | ".join(reason_parts)
                    })

    return recommendations
