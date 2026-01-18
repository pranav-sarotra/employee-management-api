"""
=============================================================================
                    EMPLOYEE PYDANTIC MODELS
=============================================================================
This module contains all Pydantic models for Employee data validation.

Key Improvements:
    - Department is now an Enum for strict validation
    - Proper field constraints with descriptive error messages
    - Separate models for Create, Update, and Response
    - Pagination support in list response
=============================================================================
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


class Department(str, Enum):
    """
    Enumeration of valid department values.
    
    Using an Enum ensures data consistency - users can only
    choose from predefined department names.
    
    Benefits:
        - No typos (e.g., "Engneering" vs "Engineering")
        - Easy to add/remove departments
        - Self-documenting API
        - Database consistency
    """
    
    ENGINEERING = "Engineering"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    HUMAN_RESOURCES = "Human Resources"
    SALES = "Sales"
    OPERATIONS = "Operations"
    INFORMATION_TECHNOLOGY = "Information Technology"
    LEGAL = "Legal"
    CUSTOMER_SERVICE = "Customer Service"
    RESEARCH = "Research and Development"


class EmployeeBase(BaseModel):
    """
    Base Pydantic model for Employee data.
    
    This model defines the core fields that every employee record must have.
    It serves as the parent class for other employee-related models.
    
    Attributes:
        employee_id: Unique identifier for the employee
        name: Full name of the employee
        age: Age of the employee (must be between 18 and 100)
        department: Department from the Department enum
    """
    
    # Employee ID - unique identifier
    employee_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z0-9_-]+$",  # Only alphanumeric, underscore, hyphen
        description="Unique identifier for the employee (e.g., EMP001)",
        examples=["EMP001", "EMP-002", "emp_003"]
    )
    
    # Employee name
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the employee",
        examples=["John Doe", "Jane Smith"]
    )
    
    # Employee age with realistic bounds
    age: int = Field(
        ...,
        ge=18,   # Minimum working age
        le=100,  # Reasonable maximum age
        description="Age of the employee (must be between 18 and 100)",
        examples=[25, 30, 45]
    )
    
    # Department - using Enum for strict validation
    department: Department = Field(
        ...,
        description="Department where the employee works",
        examples=[Department.ENGINEERING, Department.MARKETING]
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        """
        Validate and clean the employee name.
        
        - Strips leading/trailing whitespace
        - Ensures name is not just whitespace
        
        Args:
            value: The name to validate
            
        Returns:
            Cleaned name string
            
        Raises:
            ValueError: If name is empty or just whitespace
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Name cannot be empty or just whitespace")
        return cleaned
    
    # Model configuration
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employee_id": "EMP001",
                    "name": "John Doe",
                    "age": 30,
                    "department": "Engineering"
                }
            ]
        }
    }


class EmployeeCreate(EmployeeBase):
    """
    Pydantic model for creating a new employee.
    
    Inherits all fields and validation from EmployeeBase.
    Used as the request body model for POST /employees endpoint.
    """
    pass


class EmployeeUpdate(BaseModel):
    """
    Pydantic model for updating an employee (PATCH request).
    
    All fields are optional, allowing partial updates.
    Only provided fields will be updated in the database.
    
    Note: employee_id cannot be updated as it's the primary identifier.
    """
    
    # Optional name field
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Updated name of the employee"
    )
    
    # Optional age field
    age: Optional[int] = Field(
        None,
        ge=18,
        le=100,
        description="Updated age of the employee"
    )
    
    # Optional department field - also uses Enum
    department: Optional[Department] = Field(
        None,
        description="Updated department of the employee"
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        """Validate name if provided."""
        if value is not None:
            cleaned = value.strip()
            if not cleaned:
                raise ValueError("Name cannot be empty or just whitespace")
            return cleaned
        return value
    
    # Model configuration
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Jane Doe",
                    "age": 35,
                    "department": "Marketing"
                }
            ]
        }
    }


class EmployeeResponse(BaseModel):
    """
    Pydantic model for employee response.
    
    Used to format and validate API responses containing employee data.
    """
    
    employee_id: str
    name: str
    age: int
    department: Department
    
    # Model configuration
    model_config = {
        "from_attributes": True
    }


class EmployeeListResponse(BaseModel):
    """
    Pydantic model for paginated list of employees.
    
    Includes pagination metadata along with the employee list.
    
    Attributes:
        total_count: Total number of employees in database
        page: Current page number
        limit: Number of items per page
        employees: List of employee objects
    """
    
    total_count: int = Field(..., description="Total number of employees in the database")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    employees: List[EmployeeResponse] = Field(..., description="List of employees")


class MessageResponse(BaseModel):
    """
    Pydantic model for message-based API responses.
    
    Used for success/error messages in API responses.
    """
    
    message: str = Field(..., description="Response message")
    data: Optional[dict] = Field(None, description="Additional data")