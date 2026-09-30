from app.routes.incidents import router as incidents_router
from app.routes.resources import router as resources_router
from app.routes.allocations import router as allocations_router

__all__ = ["incidents_router", "resources_router", "allocations_router"]
