from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.core.logging import logger

prefix = "/api/v1"


app = FastAPI(
    title="FastAPI Social Media Backend",
    description="Backend API for posts, followers, comments, and reactions",
    version="1.0.0",
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
app.include_router(health_router, prefix=prefix)

logger.info("FastAPI application initialized")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Root Endpoint - FastAPI Application"}
