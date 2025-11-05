"""
Centralized logging configuration module.

This module provides a centralized logging setup for the entire application,
supporting both console and file outputs with rotating file handlers.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import colorlog


class LoggerManager:
    """Manages application-wide logging configuration."""

    _instance: Optional['LoggerManager'] = None
    _initialized: bool = False

    def __new__(cls):
        """Singleton pattern to ensure single logger instance."""
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize logger manager (only once)."""
        if not LoggerManager._initialized:
            self.loggers = {}
            LoggerManager._initialized = True

    def setup_logger(
            self,
            name: str,
            log_level: str = "INFO",
            log_file: Optional[str] = None,
            console_output: bool = True,
            file_output: bool = True,
            max_bytes: int = 10485760,  # 10MB
            backup_count: int = 5,
            log_format: Optional[str] = None
    ) -> logging.Logger:
        """
        Set up a logger with specified configuration.

        Args:
            name: Logger name (typically __name__ of the module)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (if file_output is True)
            console_output: Enable console output
            file_output: Enable file output
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            log_format: Custom log format string

        Returns:
            Configured logger instance
        """
        # Return existing logger if already configured
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        logger.handlers.clear()  # Clear any existing handlers

        # Default format
        if log_format is None:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Console handler with colors
        if console_output:
            console_handler = colorlog.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level.upper()))

            color_formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            console_handler.setFormatter(color_formatter)
            logger.addHandler(console_handler)

        # File handler with rotation
        if file_output and log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_formatter = logging.Formatter(
                log_format,
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

        # Cache logger
        self.loggers[name] = logger

        return logger

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get an existing logger or create a new one with default settings.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        if name in self.loggers:
            return self.loggers[name]
        return self.setup_logger(name)


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    manager = LoggerManager()
    return manager.get_logger(name)


# Example usage
if __name__ == "__main__":
    # Test logger
    test_logger = get_logger(__name__)
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message")
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    test_logger.critical("This is a critical message")
