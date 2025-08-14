"""
Logging configuration for the application.
"""
import sys
import logging
from loguru import logger
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = "app.log") -> None:
    """Set up logging configuration with both file and console outputs."""
    
    # Remove default logger
    logger.remove()
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Console logging with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        level=log_level
    )
    
    # File logging
    logger.add(
        log_dir / log_file,
        rotation="10 MB",
        retention="10 days",
        compression="gzip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level
    )
    
    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)


def get_logger(name: str):
    """Get a logger instance for the given name."""
    return logger.bind(name=name)
