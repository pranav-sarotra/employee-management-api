"""
=============================================================================
                    MODELS PACKAGE
=============================================================================
This package contains all Pydantic models for data validation.
"""

from app.models.employee import (
    Department,
    EmployeeBase,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    MessageResponse
)

__all__ = [
    "Department",
    "EmployeeBase",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "EmployeeListResponse",
    "MessageResponse"
]