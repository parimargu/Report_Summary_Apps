"""
Pytest configuration and fixtures.

Provides shared fixtures for all test modules.
"""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

import pytest
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_config():
    """Mock configuration manager."""
    from modules.config_manager import ConfigManager

    # Create a mock config
    config = ConfigManager.__new__(ConfigManager)
    ConfigManager._config = {
        'app': {
            'name': 'Test App',
            'version': '1.0.0',
            'max_file_size_mb': 5,
            'supported_formats': ['.ppt', '.pptx']
        },
        'llm': {
            'api_key': 'test_api_key',
            'model_name': 'test-model',
            'temperature': 0.3,
            'max_tokens': 1024,
            'timeout_seconds': 30,
            'max_retries': 3,
            'retry_delay_seconds': 2
        },
        'logging': {
            'level': 'INFO',
            'file': 'test.log',
            'console_output': True,
            'file_output': False
        },
        'extraction': {
            'min_table_rows': 2,
            'min_table_cols': 2
        },
        'prompts': {
            'template_file': 'prompt_template.txt',
            'system_role': 'You are a test assistant.'
        }
    }

    return config


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    data = {
        'Segment': ['Commercial', 'Retail', 'Mortgage'],
        'Q1 Default Rate (%)': [2.3, 3.1, 1.5],
        'Q2 Default Rate (%)': [2.8, 4.5, 1.6],
        'Net Rate (%)': [1.2, -0.5, 0.8]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_table_text():
    """Sample formatted table text."""
    return """
| Segment | Q1 Default Rate (%) | Q2 Default Rate (%) | Net Rate (%) |
|---------|---------------------|---------------------|--------------|
| Commercial | 2.3 | 2.8 | 1.2 |
| Retail | 3.1 | 4.5 | -0.5 |
| Mortgage | 1.5 | 1.6 | 0.8 |
    """


@pytest.fixture
def mock_presentation():
    """Mock PowerPoint presentation object."""
    presentation = MagicMock()

    # Create mock slides
    mock_slide1 = MagicMock()
    mock_slide1.shapes.title.text = "Test Slide 1"

    mock_slide2 = MagicMock()
    mock_slide2.shapes.title.text = "Test Slide 2"

    presentation.slides = [mock_slide1, mock_slide2]

    return presentation


@pytest.fixture
def mock_slide():
    """Mock PowerPoint slide object."""
    slide = MagicMock()

    # Mock title
    slide.shapes.title.text = "Test Slide"

    # Mock text shapes
    text_shape = MagicMock()
    text_shape.has_table = False
    text_shape.text = "This is sample text content."

    # Mock table shape
    table_shape = MagicMock()
    table_shape.has_table = True

    # Mock table
    mock_table = MagicMock()
    mock_row1 = MagicMock()
    mock_row1.cells = [
        MagicMock(text="Segment"),
        MagicMock(text="Rate (%)"),
    ]
    mock_row2 = MagicMock()
    mock_row2.cells = [
        MagicMock(text="Commercial"),
        MagicMock(text="2.5"),
    ]
    mock_table.rows = [mock_row1, mock_row2]
    table_shape.table = mock_table

    slide.shapes = [text_shape, table_shape]

    return slide


@pytest.fixture
def mock_groq_response():
    """Mock Groq API response."""
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = "This is a test summary."
    response.usage = MagicMock()
    response.usage.prompt_tokens = 100
    response.usage.completion_tokens = 50
    response.usage.total_tokens = 150

    return response


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_content = """
app:
  name: "Test App"
  version: "1.0.0"
  max_file_size_mb: 5
  supported_formats:
    - ".ppt"
    - ".pptx"

llm:
  provider: "groq"
  model_name: "test-model"
  temperature: 0.3
  max_tokens: 1024

logging:
  level: "INFO"
  file: "test.log"
    """

    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content)

    return str(config_file)


@pytest.fixture
def temp_prompt_file(tmp_path):
    """Create a temporary prompt template file."""
    prompt_content = """
You are a test assistant.

Analyze this table:
{table_data}

Provide a summary.
    """

    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text(prompt_content)

    return str(prompt_file)


@pytest.fixture(autouse=True)
def set_test_env():
    """Set test environment variables."""
    os.environ['GROQ_API_KEY'] = 'test_api_key_12345'
    yield
    # Cleanup
    if 'GROQ_API_KEY' in os.environ:
        del os.environ['GROQ_API_KEY']


@pytest.fixture
def mock_slide_content():
    """Mock SlideContent object."""
    from modules.content_extractor import SlideContent

    df = pd.DataFrame({
        'Segment': ['Commercial', 'Retail'],
        'Rate (%)': [2.3, 3.1]
    })

    return SlideContent(
        slide_number=1,
        title="Test Slide",
        text_content=["Sample text content"],
        tables=[df],
        table_texts=["| Segment | Rate (%) |\n|---------|----------|\n| Commercial | 2.3 |"],
        has_content=True
    )
