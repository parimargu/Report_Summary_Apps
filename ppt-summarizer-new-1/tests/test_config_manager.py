"""
Unit tests for configuration manager module.
"""

import pytest
from modules.config_manager import ConfigManager, get_config


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_singleton_pattern(self):
        """Test that ConfigManager implements singleton pattern."""
        config1 = ConfigManager()
        config2 = ConfigManager()
        assert config1 is config2

    def test_load_config_from_file(self, temp_config_file):
        """Test loading configuration from YAML file."""
        # Reset singleton
        ConfigManager._instance = None
        ConfigManager._config = {}

        config = ConfigManager(temp_config_file)

        assert config.get('app.name') == 'Test App'
        assert config.get('app.version') == '1.0.0'
        assert config.get('llm.model_name') == 'test-model'

    def test_get_with_dot_notation(self, mock_config):
        """Test getting values using dot notation."""
        assert mock_config.get('app.name') == 'Test App'
        assert mock_config.get('llm.temperature') == 0.3
        assert mock_config.get('logging.level') == 'INFO'

    def test_get_with_default(self, mock_config):
        """Test getting non-existent key returns default."""
        assert mock_config.get('non.existent.key', 'default') == 'default'
        assert mock_config.get('another.missing', None) is None

    def test_get_section(self, mock_config):
        """Test getting entire configuration section."""
        app_config = mock_config.get_section('app')

        assert isinstance(app_config, dict)
        assert 'name' in app_config
        assert 'version' in app_config
        assert app_config['name'] == 'Test App'

    def test_get_section_not_found(self, mock_config):
        """Test getting non-existent section raises KeyError."""
        with pytest.raises(KeyError):
            mock_config.get_section('non_existent_section')

    def test_set_config_value(self, mock_config):
        """Test setting configuration value."""
        mock_config.set('test.new_value', 'test_data')
        assert mock_config.get('test.new_value') == 'test_data'

    def test_set_nested_config_value(self, mock_config):
        """Test setting nested configuration value."""
        mock_config.set('new.nested.deep.value', 42)
        assert mock_config.get('new.nested.deep.value') == 42

    def test_env_variable_override(self, monkeypatch, temp_config_file):
        """Test that environment variables override config."""
        # Reset singleton
        ConfigManager._instance = None
        ConfigManager._config = {}

        # Set environment variable
        monkeypatch.setenv('LLM_MODEL_NAME', 'overridden-model')
        monkeypatch.setenv('GROQ_API_KEY', 'test_key_123')

        config = ConfigManager(temp_config_file)

        assert config.get('llm.model_name') == 'overridden-model'
        assert config.get('llm.api_key') == 'test_key_123'

    def test_config_property(self, mock_config):
        """Test accessing entire config via property."""
        full_config = mock_config.config

        assert isinstance(full_config, dict)
        assert 'app' in full_config
        assert 'llm' in full_config

    def test_convenience_function(self):
        """Test get_config convenience function."""
        config = get_config()
        assert isinstance(config, ConfigManager)


class TestConfigValidation:
    """Test configuration validation."""

    def test_missing_config_file(self):
        """Test handling of missing configuration file."""
        ConfigManager._instance = None
        ConfigManager._config = {}

        with pytest.raises(FileNotFoundError):
            ConfigManager('non_existent_config.yaml')

    def test_invalid_yaml(self, tmp_path):
        """Test handling of invalid YAML."""
        ConfigManager._instance = None
        ConfigManager._config = {}

        invalid_file = tmp_path / "invalid.yaml"
        invalid_file.write_text("invalid: yaml: content:")

        with pytest.raises(Exception):  # yaml.YAMLError
            ConfigManager(str(invalid_file))
