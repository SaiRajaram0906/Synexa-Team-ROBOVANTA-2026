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
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging
import logging

logger = setup_logging()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        req_id = str(uuid.uuid4())
        start_time = time.time()
        # Inject request_id into logger context in a real app (e.g. using contextvars)
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"[{req_id}] {request.method} {request.url.path} completed in {process_time:.4f}s", extra={"request_id": req_id})
        return response

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
