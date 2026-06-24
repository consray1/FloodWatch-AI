from app.api.v1.auth import router as auth_router
from app.api.v1.reports import router as reports_router
from app.api.v1.incidents import router as incidents_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.system import router as system_router

__all__ = [
    "auth_router",
    "reports_router",
    "incidents_router",
    "alerts_router",
    "analytics_router",
    "webhooks_router",
    "system_router"
]