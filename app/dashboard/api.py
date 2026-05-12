from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/status")
async def dashboard_status() -> dict:
    return {"status": "dashboard ready"}
