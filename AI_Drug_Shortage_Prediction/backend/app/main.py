from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.routes import (
    auth_router,
    medicines_router,
    sales_router,
    predictions_router,
    dashboard_router
)


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown
    print("🛑 Application shutting down")


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Professional API for AI Pharmacy Management System with Drug Shortage Prediction",
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth_router)
app.include_router(medicines_router)
app.include_router(sales_router)
app.include_router(predictions_router)
app.include_router(dashboard_router)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Pharmacy Management API",
        "version": settings.API_VERSION
    }


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to AI Pharmacy Management System",
        "docs": "/api/docs",
        "version": settings.API_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
