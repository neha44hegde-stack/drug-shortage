from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./pharmacy.db"
    
    # API Info
    API_TITLE: str = "AI Pharmacy Management API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Professional API for pharmacy management with AI drug shortage prediction"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]
    
    # Debug
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
