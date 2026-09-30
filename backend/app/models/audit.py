from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=True)
    details = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
