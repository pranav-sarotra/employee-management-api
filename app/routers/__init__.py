"""
=============================================================================
                    ROUTERS PACKAGE
=============================================================================
This package contains all API route handlers organized by resource.
"""

from app.routers.employees import router as employees_router

__all__ = ["employees_router"]