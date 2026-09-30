import math


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_travel_time_mins(
    distance_km: float,
    speed_kmh: float,
    accessibility: str
) -> float:
    if speed_kmh <= 0:
        speed_kmh = 25.0

    base_time_hrs = distance_km / speed_kmh

    access_multipliers = {
        "good": 1.0,
        "fair": 1.25,
        "poor": 1.75,
        "inaccessible": 2.5
    }
    multiplier = access_multipliers.get(str(accessibility).lower(), 1.25)
    
    total_mins = (base_time_hrs * 60.0) * multiplier
    return round(max(total_mins, 2.0), 1)
