from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_v1_router
from app.core.logging import logger

api_v1_router_prefix = "/api/v1"


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
app.include_router(api_v1_router, prefix=api_v1_router_prefix)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Root Endpoint - FastAPI Application"}
