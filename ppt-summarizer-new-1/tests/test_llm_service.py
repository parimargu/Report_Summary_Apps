"""
Unit tests for LLM service module.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from groq import RateLimitError, APITimeoutError, APIError

from modules.llm_service import LLMService


class TestLLMService:
    """Test cases for LLMService class."""

    @patch('modules.llm_service.Path')
    def test_initialization(self, mock_path, mock_config, temp_prompt_file):
        """Test LLMService initialization."""
        # Mock the prompt file
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        with patch('builtins.open', mock_open(read_data="Test prompt: {table_data}")):
            service = LLMService()

            assert service.model_name == 'test-model'
            assert service.temperature == 0.3
            assert service.max_tokens == 1024
            assert service.api_key == 'test_api_key'

    @patch('modules.llm_service.Path')
    def test_load_prompt_template(self, mock_path, mock_config):
        """Test loading prompt template from file."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        prompt_content = "Analyze: {table_data}"

        with patch('builtins.open', mock_open(read_data=prompt_content)):
            service = LLMService()
            assert service.prompt_template == prompt_content

    @patch('modules.llm_service.Path')
    def test_load_prompt_template_not_found(self, mock_path, mock_config):
        """Test handling of missing prompt template file."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        with pytest.raises(FileNotFoundError):
            LLMService()

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    def test_generate_summary_success(self, mock_path, mock_groq_class, mock_config, mock_groq_response):
        """Test successful summary generation."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_groq_response
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            table_data = "| A | B |\n|---|---|\n| 1 | 2 |"
            summary = service.generate_summary(table_data)

            assert summary == "This is a test summary."
            mock_client.chat.completions.create.assert_called_once()

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    @patch('time.sleep')
    def test_generate_summary_with_retry(self, mock_sleep, mock_path, mock_groq_class, mock_config, mock_groq_response):
        """Test summary generation with retry on rate limit."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        # First call raises RateLimitError, second succeeds
        mock_client.chat.completions.create.side_effect = [
            RateLimitError("Rate limit exceeded", response=Mock(), body=None),
            mock_groq_response
        ]
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            table_data = "| A | B |\n|---|---|\n| 1 | 2 |"
            summary = service.generate_summary(table_data)

            assert summary == "This is a test summary."
            assert mock_client.chat.completions.create.call_count == 2
            mock_sleep.assert_called()

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    @patch('time.sleep')
    def test_generate_summary_max_retries_exceeded(self, mock_sleep, mock_path, mock_groq_class, mock_config):
        """Test summary generation fails after max retries."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = RateLimitError(
            "Rate limit exceeded",
            response=Mock(),
            body=None
        )
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            table_data = "| A | B |\n|---|---|\n| 1 | 2 |"

            with pytest.raises(RateLimitError):
                service.generate_summary(table_data)

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    @patch('time.sleep')
    def test_generate_summary_timeout_retry(self, mock_sleep, mock_path, mock_groq_class, mock_config,
                                            mock_groq_response):
        """Test summary generation with timeout retry."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = [
            APITimeoutError("Timeout"),
            mock_groq_response
        ]
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            table_data = "| A | B |\n|---|---|\n| 1 | 2 |"
            summary = service.generate_summary(table_data)

            assert summary == "This is a test summary."
            assert mock_client.chat.completions.create.call_count == 2

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    def test_test_connection_success(self, mock_path, mock_groq_class, mock_config, mock_groq_response):
        """Test successful API connection test."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_groq_response
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            result = service.test_connection()

            assert result is True
            mock_client.chat.completions.create.assert_called()

    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    def test_test_connection_failure(self, mock_path, mock_groq_class, mock_config):
        """Test failed API connection test."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = APIError("Connection failed")
        mock_groq_class.return_value = mock_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            result = service.test_connection()

            assert result is False

    @patch('modules.llm_service.AsyncGroq')
    @patch('modules.llm_service.Groq')
    @patch('modules.llm_service.Path')
    @pytest.mark.asyncio
    async def test_generate_summary_async(self, mock_path, mock_groq_class, mock_async_groq_class, mock_config,
                                          mock_groq_response):
        """Test async summary generation."""
        # Setup mocks
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_sync_client = MagicMock()
        mock_groq_class.return_value = mock_sync_client

        mock_async_client = MagicMock()
        mock_async_client.chat.completions.create.return_value = mock_groq_response
        mock_async_groq_class.return_value = mock_async_client

        with patch('builtins.open', mock_open(read_data="Test: {table_data}")):
            service = LLMService()

            table_data = "| A | B |\n|---|---|\n| 1 | 2 |"
            summary = await service.generate_summary_async(table_data)

            assert summary == "This is a test summary."
