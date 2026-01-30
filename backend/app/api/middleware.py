"""
Custom middleware for the application
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.core.logging_config import log
from app.core.exceptions import MoodifyException
from app.config import settings
import time

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except MoodifyException as e:
            log.error(f"Moodify exception: {e.message}")
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.message, "type": type(e).__name__}
            )
        except Exception as e:
            log.error(f"Unhandled exception: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "detail": str(e)}
            )

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        log.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        duration = time.time() - start_time
        log.info(f"Response: {request.method} Status: {response.status_code} Duration: {duration:.2f}s")
        return response

def setup_middleware(app):
    # 1. Add Logging and Error Handling FIRST
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    
    # 2. Add CORS LAST (This makes it the 'outer' layer)
    # This ensures even 500 errors get the CORS headers so the browser doesn't block them
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    log.info("Middleware stack initialized (CORS outermost)")