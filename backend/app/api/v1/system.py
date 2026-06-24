from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2026-06-24T00:00:00Z"
    }


@router.get("/metrics")
async def metrics():
    return {
        "reports_total": 0,
        "incidents_active": 0,
        "alerts_pending": 0
    }