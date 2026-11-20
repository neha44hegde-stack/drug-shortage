from app.routes.auth import router as auth_router
from app.routes.medicines import router as medicines_router
from app.routes.sales import router as sales_router
from app.routes.predictions import router as predictions_router
from app.routes.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "medicines_router",
    "sales_router",
    "predictions_router",
    "dashboard_router"
]
