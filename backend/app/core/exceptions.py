from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("synexa_api")

class BaseAPIException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", "details": str(exc)}
    )

async def custom_api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
