import structlog
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.config import settings

# Configure structured logging
structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for the SMMS™ (Service Model Management System)",
    version="0.1.0",
)


@app.get("/health", summary="Health Check")
async def health_check() -> JSONResponse:
    logger.info("Health check endpoint called")
    return JSONResponse(content={"status": "ok", "app": settings.PROJECT_NAME})


# Include routers here later
# app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    # For local development
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
