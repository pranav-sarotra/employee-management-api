"""
=============================================================================
                    LOGGING CONFIGURATION
=============================================================================
This module sets up structured logging for the application.

Benefits over print():
    - Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Timestamps for each log entry
    - Can output to files, monitoring services, etc.
    - Can be easily disabled or filtered by level
    - Professional standard for production applications
=============================================================================
"""

import logging
import sys
from app.config import settings


def setup_logging() -> None:
    """
    Configure the logging system for the application.
    
    Sets up:
        - Console handler for terminal output
        - Formatting with timestamps and log levels
        - Debug level when DEBUG=true in .env
    """
    
    # Determine log level based on debug setting
    log_level = logging.DEBUG if settings.debug else logging.INFO
    
    # Create formatter with timestamp, level, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Add our handler
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name for the logger (usually __name__ of the module)
        
    Returns:
        logging.Logger: Configured logger instance
        
    Example:
        logger = get_logger(__name__)
        logger.info("This is an info message")
        logger.error("This is an error message")
    """
    return logging.getLogger(name)