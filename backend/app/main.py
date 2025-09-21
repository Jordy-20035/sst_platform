from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio

from .api.v1 import router as api_router
from .services.realtime import broadcaster

app = FastAPI(title="SST Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")


# SSE stream endpoint
async def event_generator(q: asyncio.Queue):
    try:
        while True:
            payload = await q.get()
            # SSE frame
            yield f"data: {payload}\n\n"
    except asyncio.CancelledError:
        # client disconnected
        return


@app.get("/api/v1/stream")
async def stream():
    client_id, q = await broadcaster.register()
    # remove client on disconnect
    async def gen():
        try:
            async for chunk in event_generator(q):
                yield chunk
        finally:
            await broadcaster.unregister(client_id)

    return StreamingResponse(gen(), media_type="text/event-stream")

