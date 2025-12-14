import logging
import logging.config

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.core.logging import LOGGING_CONFIG

v1_prefix = "/api/v1"


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("fastapi_app")


# Define lifespan events for startup and shutdown logging
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


# Create FastAPI application instance
app = FastAPI(
    title="FastAPI Social Media Backend",
    description="Backend API for posts, followers, comments, and reactions",
    version="1.0.0",
    lifespan=lifespan,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router, prefix=v1_prefix)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Root Endpoint - FastAPI Application"}
