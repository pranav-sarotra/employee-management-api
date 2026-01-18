"""
=============================================================================
                    EMPLOYEE MANAGEMENT API - MAIN APPLICATION
=============================================================================
Production-grade FastAPI application for managing employee information.

Version: 2.0.0

Key Features:
    - Modular architecture with separate routers
    - Dependency injection for database access
    - Environment-based configuration
    - Structured logging
    - Pagination support
    - Department validation via Enum
=============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import db_manager
from app.routers import employees_router
from app.utils.logger import setup_logging, get_logger

# Setup logging first
setup_logging()

# Get logger for this module
logger = get_logger(__name__)


# =============================================================================
# APPLICATION LIFESPAN (Startup and Shutdown)
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events:
        - On startup: Setup logging, connect to MongoDB
        - On shutdown: Disconnect from MongoDB
    
    Args:
        app: FastAPI application instance
    """
    # ========================= STARTUP =========================
    logger.info("=" * 60)
    logger.info("       STARTING EMPLOYEE MANAGEMENT API")
    logger.info("=" * 60)
    logger.info(f"Application: {settings.app_name}")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info("=" * 60)
    
    # Connect to MongoDB
    await db_manager.connect()
    
    logger.info("Application startup complete!")
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("=" * 60)
    
    yield  # Application runs here
    
    # ========================= SHUTDOWN =========================
    logger.info("=" * 60)
    logger.info("       SHUTTING DOWN EMPLOYEE MANAGEMENT API")
    logger.info("=" * 60)
    
    # Disconnect from MongoDB
    await db_manager.disconnect()
    
    logger.info("Application shutdown complete!")


# =============================================================================
# CREATE FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title=settings.app_name,
    description="""
## Employee Management API (Production-Grade)

A comprehensive, production-ready API for managing employee information.

### Features
* **CRUD Operations** - Create, Read, Update, Delete employees
* **Pagination** - Efficiently handle large datasets
* **Department Filtering** - Filter employees by department
* **Input Validation** - Strict validation using Pydantic
* **Structured Logging** - Professional logging system
* **Dependency Injection** - Testable and maintainable code

### Departments
Employees can belong to one of the following departments:
- Engineering
- Marketing
- Finance
- Human Resources
- Sales
- Operations
- IT
- Legal
- Customer Service
- Research and Development
    """,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License"
    }
)


# =============================================================================
# MIDDLEWARE
# =============================================================================

# Add CORS middleware (allows frontend applications to call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# INCLUDE ROUTERS
# =============================================================================

# Include the employees router
app.include_router(employees_router)


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Welcome endpoint with API information"
)
async def root():
    """
    Root endpoint that returns API information.
    """
    logger.debug("Root endpoint accessed")
    
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "documentation": "/docs",
        "endpoints": {
            "create_employee": "POST /employees",
            "list_employees": "GET /employees?page=1&limit=10",
            "get_employee": "GET /employees/{employee_id}",
            "update_employee": "PATCH /employees/{employee_id}",
            "delete_employee": "DELETE /employees/{employee_id}",
            "list_departments": "GET /employees/meta/departments"
        }
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Check API and database health status"
)
async def health_check():
    """
    Health check endpoint to verify API and database status.
    """
    logger.debug("Health check requested")
    
    try:
        # Check MongoDB connection
        await db_manager.client.admin.command("ping")
        db_status = "healthy"
        logger.debug("Database health check: healthy")
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        logger.error(f"Database health check failed: {str(e)}")
    
    return {
        "status": "running",
        "version": settings.app_version,
        "database": db_status
    }