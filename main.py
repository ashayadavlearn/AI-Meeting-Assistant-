import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal, init_db
from app.routers import (
    auth_router,
    meetings_router,
    tasks_router,
    chat_router,
    analytics_router,
    search_router
)

# Initialize database schema and pre-seed sample data immediately
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MeetBuddy AI - Your Intelligent Meeting Assistant SaaS API",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(meetings_router.router, prefix=settings.API_V1_STR)
app.include_router(tasks_router.router, prefix=settings.API_V1_STR)
app.include_router(chat_router.router, prefix=settings.API_V1_STR)
app.include_router(analytics_router.router, prefix=settings.API_V1_STR)
app.include_router(search_router.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "app": "MeetBuddy AI",
        "tagline": "Transform meetings into organized actions with AI",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MeetBuddy AI Backend"}
