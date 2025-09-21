from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentOut
from app.crud.incident import create_incident, get_incidents, get_incident
from app.services.realtime import broadcaster
from app.core.security import decode_access_token

router = APIRouter()
# GET /api/v1/incidents
@router.get("/", response_model=List[IncidentOut])
def list_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_incidents(db, skip=skip, limit=limit)


# POST /api/v1/incidents
@router.post("/", response_model=IncidentOut)
def post_incident(incident_in: IncidentCreate, request: Request, db: Session = Depends(get_db)):
    # try to get optional token for reporter_id (Bearer <token>)
    reporter_id = None
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1]
        payload = decode_access_token(token)
        if payload and "sub" in payload:
            try:
                reporter_id = int(payload["sub"])
            except Exception:
                reporter_id = None

    db_inc = create_incident(db, incident_in=incident_in, reporter_id=reporter_id)
    # push to SSE broadcaster (non-blocking)
    import asyncio
    asyncio.create_task(broadcaster.publish({
        "type": "incident.created",
        "data": {
            "id": db_inc.id,
            "title": db_inc.title,
            "status": db_inc.status,
            "latitude": db_inc.latitude,
            "longitude": db_inc.longitude,
            "created_at": str(db_inc.created_at)
        }
    }))
    return db_inc


# GET /api/v1/incidents/{id}
@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident_by_id(incident_id: int, db: Session = Depends(get_db)):
    db_inc = get_incident(db, incident_id)
    if not db_inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return db_inc

