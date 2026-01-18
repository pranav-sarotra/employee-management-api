"""
=============================================================================
                    DATABASE CONNECTION & DEPENDENCY INJECTION
=============================================================================
This module handles MongoDB connection management using dependency injection.

Key Improvements:
    - Uses FastAPI's Depends for dependency injection
    - Makes the code testable (can mock the database in tests)
    - Proper connection lifecycle management
    - No global state that's hard to manage
=============================================================================
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.config import settings
from app.utils.logger import get_logger

# Get logger for this module
logger = get_logger(__name__)


class DatabaseManager:
    """
    Manages MongoDB database connections.
    
    This class handles the lifecycle of database connections,
    providing methods to connect, disconnect, and access collections.
    
    Attributes:
        client: MongoDB async client instance
        database: Database reference
        collection: Employees collection reference
    """
    
    def __init__(self):
        """Initialize the database manager with no active connection."""
        self.client: AsyncIOMotorClient = None
        self.database = None
        self.collection: AsyncIOMotorCollection = None
    
    async def connect(self) -> None:
        """
        Establish connection to MongoDB.
        
        Creates an async MongoDB client and sets up references
        to the database and employees collection.
        Also creates a unique index on employee_id.
        
        Raises:
            Exception: If connection fails
        """
        logger.info("Connecting to MongoDB...")
        logger.debug(f"MongoDB URL: {settings.mongodb_url}")
        logger.debug(f"Database: {settings.database_name}")
        logger.debug(f"Collection: {settings.collection_name}")
        
        try:
            # Create async MongoDB client
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            
            # Get database reference
            self.database = self.client[settings.database_name]
            
            # Get collection reference
            self.collection = self.database[settings.collection_name]
            
            # Create unique index on employee_id for data integrity
            # This is crucial for preventing duplicate IDs at the database level
            await self.collection.create_index("employee_id", unique=True)
            
            # Test connection by pinging the server
            await self.client.admin.command("ping")
            
            logger.info("Successfully connected to MongoDB!")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """
        Close MongoDB connection.
        
        Properly closes the MongoDB client connection
        to prevent resource leaks.
        """
        logger.info("Disconnecting from MongoDB...")
        
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
            self.collection = None
            
        logger.info("MongoDB connection closed!")
    
    def get_collection(self) -> AsyncIOMotorCollection:
        """
        Get the employees collection.
        
        Returns:
            AsyncIOMotorCollection: The employees collection
            
        Raises:
            RuntimeError: If database is not connected
        """
        if self.collection is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.collection


# Create a single instance of DatabaseManager
# This will be used throughout the application
db_manager = DatabaseManager()


async def get_database() -> AsyncIOMotorCollection:
    """
    Dependency injection function for database collection.
    
    This function is used with FastAPI's Depends() to inject
    the database collection into endpoint functions.
    
    Benefits:
        - Makes endpoints testable (can mock this dependency)
        - Centralizes database access
        - Clear dependency declaration in function signatures
    
    Returns:
        AsyncIOMotorCollection: The employees collection
        
    Example:
        @app.get("/employees")
        async def get_employees(db: AsyncIOMotorCollection = Depends(get_database)):
            # Use db here
            pass
    """
    return db_manager.get_collection()