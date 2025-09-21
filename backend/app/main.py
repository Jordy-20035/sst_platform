from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# Allow frontend to connect
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incident model
class Incident(BaseModel):
    id: int
    title: str
    description: str = ""
    latitude: float
    longitude: float
    status: str = "reported"
    timestamp: float = time.time()

# In-memory incidents list (demo purposes)
incidents: List[Incident] = [
    Incident(id=1, title="Pothole on Main St.", latitude=54.787, longitude=32.048, status="active"),
    Incident(id=2, title="Traffic jam", latitude=54.788, longitude=32.050, status="reported")
]

# SSE subscribers
subscribers = []

@app.get("/api/v1/incidents")
async def get_incidents():
    return incidents

@app.post("/api/v1/incidents")
async def create_incident(incident: Incident):
    incidents.append(incident)
    # notify SSE subscribers
    for queue in subscribers:
        await queue.put({"type": "incident.created", "data": incident.dict()})
    return incident

@app.get("/api/v1/stream")
async def stream(request: Request):
    q = asyncio.Queue()
    subscribers.append(q)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                item = await q.get()
                yield {"event": "message", "data": item}
        finally:
            subscribers.remove(q)

    return EventSourceResponse(event_generator())
