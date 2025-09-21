from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_incidents():
    return [{"id": 1, "location": "Main St", "status": "active"}]
