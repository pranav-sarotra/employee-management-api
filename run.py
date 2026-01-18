"""
=============================================================================
                    APPLICATION RUNNER
=============================================================================
Script to run the FastAPI application using Uvicorn.

Usage:
    python run.py
    
The application will start on http://localhost:8000
=============================================================================
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print(f"       {settings.app_name}")
    print("=" * 60)
    print(f"Version: {settings.app_version}")
    print(f"Debug Mode: {settings.debug}")
    print("=" * 60)
    print("Starting server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs:  http://localhost:8000/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug  # Auto-reload only in debug mode
    )