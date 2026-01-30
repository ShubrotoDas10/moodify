from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.core.logging_config import log
from app.models.ml_models.model_loader import model_manager
from app.api.middleware import setup_middleware
from app.api.routes import health, audio, image, chat
from app.utils.file_handlers import cleanup_old_files
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting Moodify backend...")
    try:
        model_manager.load_all_models()
        cleanup_task = asyncio.create_task(periodic_cleanup())
        yield
    finally:
        cleanup_task.cancel()
        log.info("Moodify backend shut down")

async def periodic_cleanup():
    while True:
        try:
            await asyncio.sleep(3600)
            cleanup_old_files()
        except asyncio.CancelledError:
            break
        except Exception as e:
            log.error(f"Cleanup error: {e}")

app = FastAPI(title="Moodify API", lifespan=lifespan)

# Initialize Middleware
setup_middleware(app)

# Include Routers
app.include_router(health.router)
app.include_router(audio.router)
app.include_router(image.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Moodify API Active", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )