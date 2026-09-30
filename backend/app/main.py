from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes.incidents import router as incidents_router
from app.routes.resources import router as resources_router
from app.routes.allocations import router as allocations_router
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FloodMesh AI API",
    description="Dynamic AI-Powered Emergency Resource Allocation Platform for Flood Response",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents_router)
app.include_router(resources_router)
app.include_router(allocations_router)


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "FloodMesh AI Backend",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )
