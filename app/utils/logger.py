import logging
import sys
from typing import Optional

def configure_logger(name: str = "neo_benchlab", level: str = "INFO") -> logging.Logger:
    """Configure and return a logger with console and optional file handlers."""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Formatter with detailed info
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str = "neo_benchlab") -> logging.Logger:
    """Get an existing logger or configure a new one."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return configure_logger(name)
    return logger
