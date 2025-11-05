"""
Configuration management module.

Handles loading and accessing configuration from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

from modules.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """Manages application configuration from YAML and environment variables."""

    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Singleton pattern to ensure single configuration instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to the configuration YAML file
        """
        if not ConfigManager._config:  # Only load once
            self._load_config(config_path)
            self._load_env_variables()
            logger.info("Configuration loaded successfully")

    def _load_config(self, config_path: str) -> None:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        config_file = Path(config_path)

        if not config_file.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                ConfigManager._config = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise

    def _load_env_variables(self) -> None:
        """Load environment variables from .env file and system."""
        load_dotenv()

        # Override config with environment variables if present
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            if "llm" not in ConfigManager._config:
                ConfigManager._config["llm"] = {}
            ConfigManager._config["llm"]["api_key"] = groq_key
            logger.info("Loaded GROQ_API_KEY from environment")

        # Additional environment variable overrides
        env_overrides = {
            "LLM_MODEL_NAME": ("llm", "model_name"),
            "LLM_TEMPERATURE": ("llm", "temperature"),
            "LLM_MAX_TOKENS": ("llm", "max_tokens"),
            "LOG_LEVEL": ("logging", "level"),
            "MAX_FILE_SIZE_MB": ("app", "max_file_size_mb"),
        }

        for env_var, (section, key) in env_overrides.items():
            value = os.getenv(env_var)
            if value:
                if section not in ConfigManager._config:
                    ConfigManager._config[section] = {}

                # Type conversion
                try:
                    if key in ["temperature", "max_file_size_mb"]:
                        value = float(value)
                    elif key in ["max_tokens"]:
                        value = int(value)

                    ConfigManager._config[section][key] = value
                    logger.info(f"Override {section}.{key} from environment: {value}")
                except ValueError as e:
                    logger.warning(f"Failed to convert {env_var}: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Configuration key path (e.g., "app.name" or "llm.model_name")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config = ConfigManager()
            >>> config.get("app.name")
            'PowerPoint Content Summarization'
            >>> config.get("llm.model_name")
            'llama-3.1-70b-versatile'
        """
        keys = key_path.split('.')
        value = ConfigManager._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Configuration key '{key_path}' not found, using default: {default}")
            return default

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.

        Args:
            section: Section name (e.g., "app", "llm", "logging")

        Returns:
            Dictionary containing section configuration

        Raises:
            KeyError: If section doesn't exist
        """
        if section not in ConfigManager._config:
            logger.error(f"Configuration section '{section}' not found")
            raise KeyError(f"Configuration section '{section}' not found")

        return ConfigManager._config[section]

    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key_path: Configuration key path
            value: Value to set
        """
        keys = key_path.split('.')
        config = ConfigManager._config

        # Navigate to the parent dictionary
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Set the value
        config[keys[-1]] = value
        logger.debug(f"Set configuration: {key_path} = {value}")

    @property
    def config(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return ConfigManager._config

    def reload(self, config_path: str = "config.yaml") -> None:
        """
        Reload configuration from file.

        Args:
            config_path: Path to configuration file
        """
        ConfigManager._config = {}
        self._load_config(config_path)
        self._load_env_variables()
        logger.info("Configuration reloaded")


# Convenience function
def get_config() -> ConfigManager:
    """
    Get ConfigManager instance.

    Returns:
        ConfigManager singleton instance
    """
    return ConfigManager()


# Example usage
if __name__ == "__main__":
    config = get_config()
    print(f"App Name: {config.get('app.name')}")
    print(f"LLM Model: {config.get('llm.model_name')}")
    print(f"Log Level: {config.get('logging.level')}")
    print(f"\nFull App Config: {config.get_section('app')}")
