"""
=============================================================================
                    EMPLOYEE API ROUTES
=============================================================================
This module contains all CRUD endpoints for employee management.

Key Improvements:
    - Uses APIRouter for modular organization
    - Dependency injection for database access
    - Catches DuplicateKeyError for race condition safety
    - PATCH instead of PUT for partial updates
    - Pagination support for listing employees
=============================================================================
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from app.database import get_database
from app.models.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    MessageResponse,
    Department
)
from app.utils.logger import get_logger

# Get logger for this module
logger = get_logger(__name__)

# Create router with prefix and tags
router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={
        404: {"description": "Employee not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)


# =============================================================================
# CREATE EMPLOYEE (POST)
# =============================================================================

@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Add a new employee to the database. Employee ID must be unique."
)
async def create_employee(
    employee: EmployeeCreate,
    db: AsyncIOMotorCollection = Depends(get_database)
):
    """
    Create a new employee record in the database.
    
    This endpoint uses database-level unique constraint to handle
    duplicate IDs, preventing race conditions that could occur
    with check-then-insert logic.
    
    Args:
        employee: Employee data from request body
        db: Database collection (injected via Depends)
    
    Returns:
        MessageResponse: Success message with created employee data
        
    Raises:
        HTTPException 400: If Employee ID already exists
        HTTPException 500: If database operation fails
    """
    logger.info(f"Creating employee with ID: {employee.employee_id}")
    
    # Prepare employee document
    # Convert Enum to string value for MongoDB storage
    employee_dict = employee.model_dump()
    employee_dict["department"] = employee.department.value
    
    try:
        # Attempt to insert - MongoDB will raise DuplicateKeyError if ID exists
        # This is safer than check-then-insert due to race conditions
        result = await db.insert_one(employee_dict)
        
        if result.inserted_id:
            logger.info(f"Successfully created employee: {employee.employee_id}")
            
            # Remove MongoDB's _id from response
            employee_dict.pop("_id", None)
            
            return MessageResponse(
                message="Employee created successfully",
                data={"employee": employee_dict}
            )
        else:
            logger.error(f"Failed to create employee: {employee.employee_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create employee"
            )
            
    except DuplicateKeyError:
        # This catches the race condition - two requests trying to create
        # the same ID simultaneously
        logger.warning(f"Duplicate employee ID attempted: {employee.employee_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID '{employee.employee_id}' already exists"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error while creating employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


# =============================================================================
# READ ALL EMPLOYEES (GET) - With Pagination
# =============================================================================

@router.get(
    "",
    response_model=EmployeeListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all employees (paginated)",
    description="Retrieve a paginated list of all employees from the database."
)
async def get_all_employees(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number (starts from 1)"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of employees per page (max 100)"
    ),
    department: Department = Query(
        default=None,
        description="Filter by department (optional)"
    ),
    db: AsyncIOMotorCollection = Depends(get_database)
):
    """
    Retrieve all employee records with pagination support.
    
    Pagination prevents performance issues when dealing with
    large datasets. Instead of returning all 10,000 employees,
    we return them in pages of 10-100 at a time.
    
    Args:
        page: Page number (1-indexed)
        limit: Number of items per page (1-100)
        department: Optional department filter
        db: Database collection (injected via Depends)
    
    Returns:
        EmployeeListResponse: Paginated list of employees with metadata
    """
    logger.info(f"Fetching employees - Page: {page}, Limit: {limit}")
    
    try:
        # Build query filter
        query_filter = {}
        if department:
            query_filter["department"] = department.value
            logger.debug(f"Filtering by department: {department.value}")
        
        # Calculate skip value for pagination
        skip = (page - 1) * limit
        
        # Get total count for pagination metadata
        total_count = await db.count_documents(query_filter)
        
        # Fetch employees with pagination
        cursor = db.find(
            query_filter,
            {"_id": 0}  # Exclude MongoDB's internal _id field
        ).skip(skip).limit(limit)
        
        employees = await cursor.to_list(length=limit)
        
        logger.info(f"Found {len(employees)} employees (Total: {total_count})")
        
        return EmployeeListResponse(
            total_count=total_count,
            page=page,
            limit=limit,
            employees=employees
        )
        
    except Exception as e:
        logger.error(f"Database error while fetching employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


# =============================================================================
# READ SINGLE EMPLOYEE (GET by ID)
# =============================================================================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID",
    description="Retrieve a specific employee's details using their Employee ID."
)
async def get_employee(
    employee_id: str,
    db: AsyncIOMotorCollection = Depends(get_database)
):
    """
    Retrieve a specific employee by their Employee ID.
    
    Args:
        employee_id: The unique identifier of the employee
        db: Database collection (injected via Depends)
    
    Returns:
        EmployeeResponse: Employee object with all details
        
    Raises:
        HTTPException 404: If employee is not found
    """
    logger.info(f"Fetching employee with ID: {employee_id}")
    
    try:
        employee = await db.find_one(
            {"employee_id": employee_id},
            {"_id": 0}
        )
        
        if not employee:
            logger.warning(f"Employee not found: {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )
        
        logger.info(f"Found employee: {employee_id}")
        return EmployeeResponse(**employee)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error while fetching employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


# =============================================================================
# UPDATE EMPLOYEE (PATCH) - Partial Update
# =============================================================================

@router.patch(
    "/{employee_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Update employee (partial)",
    description="Update specific fields of an existing employee. Only provided fields will be updated."
)
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    db: AsyncIOMotorCollection = Depends(get_database)
):
    """
    Update an existing employee's information (partial update).
    
    Uses PATCH instead of PUT because we support partial updates.
    PUT semantically means "replace entire resource" while
    PATCH means "modify specific fields".
    
    Args:
        employee_id: The unique identifier of the employee to update
        employee_update: Fields to update (all optional)
        db: Database collection (injected via Depends)
    
    Returns:
        MessageResponse: Success message with updated employee data
        
    Raises:
        HTTPException 400: If no valid fields provided
        HTTPException 404: If employee is not found
    """
    logger.info(f"Updating employee: {employee_id}")
    
    try:
        # Check if employee exists
        existing_employee = await db.find_one({"employee_id": employee_id})
        
        if not existing_employee:
            logger.warning(f"Employee not found for update: {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )
        
        # Build update document with only non-None values
        update_data = {}
        for key, value in employee_update.model_dump().items():
            if value is not None:
                # Convert Enum to string for MongoDB
                if isinstance(value, Department):
                    update_data[key] = value.value
                else:
                    update_data[key] = value
        
        # Check if there are any fields to update
        if not update_data:
            logger.warning(f"No fields provided for update: {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for update. "
                       "Please provide at least one of: name, age, department"
            )
        
        logger.debug(f"Update data: {update_data}")
        
        # Perform update
        await db.update_one(
            {"employee_id": employee_id},
            {"$set": update_data}
        )
        
        # Fetch updated employee
        updated_employee = await db.find_one(
            {"employee_id": employee_id},
            {"_id": 0}
        )
        
        logger.info(f"Successfully updated employee: {employee_id}")
        
        return MessageResponse(
            message="Employee updated successfully",
            data={"employee": updated_employee}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error while updating employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


# =============================================================================
# DELETE EMPLOYEE (DELETE)
# =============================================================================

@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete employee",
    description="Remove an employee from the database."
)
async def delete_employee(
    employee_id: str,
    db: AsyncIOMotorCollection = Depends(get_database)
):
    """
    Delete an employee from the database.
    
    Args:
        employee_id: The unique identifier of the employee to delete
        db: Database collection (injected via Depends)
    
    Returns:
        MessageResponse: Success message confirming deletion
        
    Raises:
        HTTPException 404: If employee is not found
    """
    logger.info(f"Deleting employee: {employee_id}")
    
    try:
        # Check if employee exists
        existing_employee = await db.find_one({"employee_id": employee_id})
        
        if not existing_employee:
            logger.warning(f"Employee not found for deletion: {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID '{employee_id}' not found"
            )
        
        # Perform deletion
        result = await db.delete_one({"employee_id": employee_id})
        
        if result.deleted_count == 1:
            logger.info(f"Successfully deleted employee: {employee_id}")
            return MessageResponse(
                message="Employee deleted successfully",
                data={"deleted_employee_id": employee_id}
            )
        else:
            logger.error(f"Failed to delete employee: {employee_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete employee"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error while deleting employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


# =============================================================================
# GET AVAILABLE DEPARTMENTS (Utility Endpoint)
# =============================================================================

@router.get(
    "/meta/departments",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get available departments",
    description="Retrieve the list of valid department values."
)
async def get_departments():
    """
    Return list of valid department values.
    
    This is a utility endpoint that helps API consumers
    know what department values are acceptable.
    
    Returns:
        dict: List of department names
    """
    logger.debug("Fetching available departments")
    
    return {
        "departments": [dept.value for dept in Department]
    }