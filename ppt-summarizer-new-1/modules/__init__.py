"""
Modules package for PowerPoint Content Summarization Application.

This package contains all core functionality modules including:
- Configuration management
- File parsing
- Content extraction
- LLM service integration
- UI rendering
- Logging
"""
'''
__version__ = "1.0.0"
__author__ = "PowerPoint Summarizer Team"

from modules.config_manager import ConfigManager, get_config
from modules.file_parser import FileParser
from modules.content_extractor import ContentExtractor, SlideContent
from modules.llm_service import LLMService
from modules.ui_renderer import UIRenderer
from modules.logger import LoggerManager, get_logger

__all__ = [
    'ConfigManager',
    'get_config',
    'FileParser',
    'ContentExtractor',
    'SlideContent',
    'LLMService',
    'UIRenderer',
    'LoggerManager',
    'get_logger',
]
'''