"""
=============================================================================
                    CONFIGURATION MANAGEMENT
=============================================================================
This module handles all application configuration using pydantic-settings.
Configuration values are loaded from environment variables or .env file.

Benefits:
    - No hardcoded credentials
    - Easy to change between environments (dev, staging, production)
    - Type validation for configuration values
    - Secure handling of sensitive data
=============================================================================
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        mongodb_url: MongoDB connection string
        database_name: Name of the MongoDB database
        collection_name: Name of the employees collection
        app_name: Application name for documentation
        app_version: Application version
        debug: Debug mode flag
    """
    
    # -------------------------------------------------------------------------
    # MongoDB Configuration
    # -------------------------------------------------------------------------
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "employee_management"
    collection_name: str = "employees"
    
    # -------------------------------------------------------------------------
    # Application Configuration
    # -------------------------------------------------------------------------
    app_name: str = "Employee Management API"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # -------------------------------------------------------------------------
    # Pydantic Settings Configuration
    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8", # File encoding
        case_sensitive=False,      # Environment variables are case-insensitive
        extra="ignore"             # Ignore extra environment variables
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once,
    improving performance by avoiding repeated file reads.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Create a global settings instance for easy access
settings = get_settings()