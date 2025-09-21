from pydantic import BaseModel, Field
from datetime import datetime


class IncidentBase(BaseModel):
    title: str = Field(..., example="Pothole on Central Ave")
    description: str | None = None
    status: str | None = "reported"
    latitude: float | None = None
    longitude: float | None = None


class IncidentCreate(IncidentBase):
    pass


class IncidentOut(IncidentBase):
    id: int
    reporter_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
