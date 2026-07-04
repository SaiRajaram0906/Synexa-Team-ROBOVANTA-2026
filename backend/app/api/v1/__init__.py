from fastapi import APIRouter
from .auth import router as auth_router
from .business import router as business_router
from .analysis import router as analysis_router
from .dashboard import router as dashboard_router
from .copilot import router as copilot_router
from .analytics import router as analytics_router
from .documents import router as documents_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(business_router, prefix="/business", tags=["Business"])
router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(copilot_router, prefix="/copilot", tags=["Copilot"])
router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
router.include_router(documents_router, prefix="/documents", tags=["Documents"])
