from sqlalchemy.orm import Session
from typing import List
from ..models.incident import Incident
from ..schemas.incident import IncidentCreate


def create_incident(db: Session, incident_in: IncidentCreate, reporter_id: int | None = None) -> Incident:
    db_inc = Incident(
        title=incident_in.title,
        description=incident_in.description,
        status=incident_in.status or "reported",
        latitude=incident_in.latitude,
        longitude=incident_in.longitude,
        reporter_id=reporter_id,
    )
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)
    return db_inc


def get_incidents(db: Session, skip: int = 0, limit: int = 100) -> List[Incident]:
    return db.query(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()


def get_incident(db: Session, incident_id: int) -> Incident | None:
    return db.query(Incident).filter(Incident.id == incident_id).first()
