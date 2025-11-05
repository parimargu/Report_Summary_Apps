"""
Unit tests for file parser module.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

from modules.file_parser import FileParser


class TestFileParser:
    """Test cases for FileParser class."""

    def test_initialization(self, mock_config):
        """Test FileParser initialization."""
        parser = FileParser()

        assert parser.max_file_size_mb == 5
        assert '.pptx' in parser.supported_formats
        assert '.ppt' in parser.supported_formats

    def test_validate_file_not_found(self, mock_config):
        """Test validation of non-existent file."""
        parser = FileParser()

        is_valid, error = parser.validate_file('non_existent_file.pptx')

        assert is_valid is False
        assert error is not None
        assert 'not found' in error.lower()

    def test_validate_file_unsupported_format(self, mock_config, tmp_path):
        """Test validation of unsupported file format."""
        parser = FileParser()

        # Create a test file with wrong extension
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")

        is_valid, error = parser.validate_file(str(test_file))

        assert is_valid is False
        assert 'unsupported' in error.lower()

    def test_validate_file_too_large(self, mock_config, tmp_path):
        """Test validation of file that's too large."""
        parser = FileParser()

        # Create a large test file (> 5MB)
        test_file = tmp_path / "large.pptx"
        large_content = 'x' * (6 * 1024 * 1024)  # 6MB
        test_file.write_text(large_content)

        is_valid, error = parser.validate_file(str(test_file))

        assert is_valid is False
        assert 'exceeds' in error.lower()

    def test_validate_file_success(self, mock_config, tmp_path):
        """Test successful file validation."""
        parser = FileParser()

        # Create a valid test file
        test_file = tmp_path / "valid.pptx"
        test_file.write_text("test content")

        is_valid, error = parser.validate_file(str(test_file))

        assert is_valid is True
        assert error is None

    def test_validate_uploaded_file_unsupported(self, mock_config):
        """Test validation of uploaded file with unsupported format."""
        parser = FileParser()

        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.size = 1024

        is_valid, error = parser.validate_uploaded_file(mock_file)

        assert is_valid is False
        assert 'unsupported' in error.lower()

    def test_validate_uploaded_file_too_large(self, mock_config):
        """Test validation of uploaded file that's too large."""
        parser = FileParser()

        mock_file = Mock()
        mock_file.name = "large.pptx"
        mock_file.size = 6 * 1024 * 1024  # 6MB

        is_valid, error = parser.validate_uploaded_file(mock_file)

        assert is_valid is False
        assert 'exceeds' in error.lower()

    def test_validate_uploaded_file_success(self, mock_config):
        """Test successful uploaded file validation."""
        parser = FileParser()

        mock_file = Mock()
        mock_file.name = "valid.pptx"
        mock_file.size = 1024 * 1024  # 1MB

        is_valid, error = parser.validate_uploaded_file(mock_file)

        assert is_valid is True
        assert error is None

    @patch('modules.file_parser.Presentation')
    def test_parse_presentation_success(self, mock_prs_class, mock_config, tmp_path):
        """Test successful presentation parsing."""
        parser = FileParser()

        # Create a valid test file
        test_file = tmp_path / "test.pptx"
        test_file.write_text("test content")

        # Mock Presentation
        mock_prs = MagicMock()
        mock_prs.slides = [Mock(), Mock(), Mock()]
        mock_prs_class.return_value = mock_prs

        result = parser.parse_presentation(str(test_file))

        assert result is not None
        mock_prs_class.assert_called_once_with(str(test_file))

    def test_parse_presentation_invalid_file(self, mock_config):
        """Test parsing non-existent presentation."""
        parser = FileParser()

        with pytest.raises((ValueError, FileNotFoundError)):
            parser.parse_presentation('non_existent.pptx')

    @patch('modules.file_parser.Presentation')
    def test_parse_uploaded_presentation(self, mock_prs_class, mock_config):
        """Test parsing uploaded presentation."""
        parser = FileParser()

        # Mock uploaded file
        mock_file = Mock()
        mock_file.name = "uploaded.pptx"
        mock_file.size = 1024 * 1024

        # Mock Presentation
        mock_prs = MagicMock()
        mock_prs.slides = [Mock(), Mock()]
        mock_prs_class.return_value = mock_prs

        result = parser.parse_uploaded_presentation(mock_file)

        assert result is not None
        mock_prs_class.assert_called_once()

    def test_get_slide_count(self, mock_config, mock_presentation):
        """Test getting slide count from presentation."""
        parser = FileParser()

        count = parser.get_slide_count(mock_presentation)

        assert count == 2

    def test_get_slide_count_error(self, mock_config):
        """Test getting slide count with error."""
        parser = FileParser()

        invalid_prs = Mock()
        invalid_prs.slides = None

        count = parser.get_slide_count(invalid_prs)

        assert count == 0
