from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.business import router as business_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.strategy import router as strategy_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.documents import router as documents_router

app = FastAPI(title="Synexa Growth OS API")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(business_router, prefix="/api/v1/business", tags=["Business"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(strategy_router, prefix="/api/v1/strategy", tags=["Strategy"])
app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["Copilot"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(documents_router, prefix="/api/v1/documents", tags=["Documents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
