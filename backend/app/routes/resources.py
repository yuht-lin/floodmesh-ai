import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resource import Resource

router = APIRouter(prefix="/resources", tags=["Resources"])


# Pydantic schema for creating/updating resources
class ResourceCreateRequest(BaseModel):
    name: str = Field(..., description="Name of rescue unit e.g. 'NDRF Boat Alpha'")
    resource_type: Optional[str] = Field("rescue_boat", description="rescue_boat, ambulance, police_unit, camp")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    capacity: Optional[int] = Field(10, description="Max capacity in persons")
    status: Optional[str] = Field("available", description="available, assigned, maintenance")


@router.get("")
@router.get("/")
async def get_all_resources(db: Session = Depends(get_db)):
    """Fetches all rescue resources from floodmesh.db formatted cleanly for React Frontend."""
    try:
        resources = db.query(Resource).all()
        output = []

        for res in resources:
            # Safe extraction of ID and Type regardless of DB column naming
            res_id = (
                getattr(res, "resource_id", None) or 
                getattr(res, "id", None) or 
                "RES-000"
            )
            res_type = (
                getattr(res, "resource_type", None) or 
                getattr(res, "type", None) or 
                "rescue_boat"
            )

            output.append({
                "id": str(res_id),
                "resource_id": str(res_id),
                "name": str(getattr(res, "name", f"Resource #{res_id}")),
                "type": str(res_type),
                "resource_type": str(res_type),
                "latitude": float(res.latitude),
                "longitude": float(res.longitude),
                "capacity": int(getattr(res, "capacity", 10) or 10),
                "status": str(getattr(res, "status", "available") or "available"),
            })

        return output
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch resources: {str(err)}",
        )


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(payload: ResourceCreateRequest, db: Session = Depends(get_db)):
    """Adds a new rescue resource (boat, ambulance, police squad) to the database."""
    gen_id = f"RES-{uuid.uuid4().hex[:6].upper()}"

    try:
        new_res = Resource()

        # Dynamic attribute assignment for database compatibility
        if hasattr(new_res, "resource_id"):
            setattr(new_res, "resource_id", gen_id)
        if hasattr(new_res, "id"):
            setattr(new_res, "id", gen_id)

        if hasattr(new_res, "resource_type"):
            setattr(new_res, "resource_type", payload.resource_type)
        if hasattr(new_res, "type"):
            setattr(new_res, "type", payload.resource_type)

        setattr(new_res, "name", payload.name)
        setattr(new_res, "latitude", float(payload.latitude))
        setattr(new_res, "longitude", float(payload.longitude))
        setattr(new_res, "capacity", int(payload.capacity or 10))
        setattr(new_res, "status", str(payload.status or "available"))

        db.add(new_res)
        db.commit()
        db.refresh(new_res)

        return {
            "status": "success",
            "message": "Rescue resource created successfully",
            "resource": {
                "id": gen_id,
                "resource_id": gen_id,
                "name": payload.name,
                "type": payload.resource_type,
                "resource_type": payload.resource_type,
                "latitude": float(payload.latitude),
                "longitude": float(payload.longitude),
                "capacity": payload.capacity,
                "status": payload.status,
            },
        }
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create resource: {str(err)}",
        )


@router.get("/{resource_id}")
async def get_resource_by_id(resource_id: str, db: Session = Depends(get_db)):
    """Fetches a single rescue unit by its unique resource_id or id."""
    resource = None
    if hasattr(Resource, "resource_id"):
        resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()
    if not resource and hasattr(Resource, "id"):
        resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource '{resource_id}' not found.",
        )

    res_id = getattr(resource, "resource_id", getattr(resource, "id", resource_id))
    res_type = getattr(resource, "resource_type", getattr(resource, "type", "rescue_boat"))

    return {
        "id": str(res_id),
        "resource_id": str(res_id),
        "name": str(getattr(resource, "name", f"Resource #{res_id}")),
        "type": str(res_type),
        "resource_type": str(res_type),
        "latitude": float(resource.latitude),
        "longitude": float(resource.longitude),
        "capacity": int(getattr(resource, "capacity", 10) or 10),
        "status": str(getattr(resource, "status", "available") or "available"),
    }
