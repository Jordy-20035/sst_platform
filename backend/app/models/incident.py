from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from ..db.base import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String(50), nullable=False, default="reported")  # reported, active, resolved
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
