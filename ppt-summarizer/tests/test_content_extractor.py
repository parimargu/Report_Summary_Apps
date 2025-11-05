"""
Unit tests for content extractor module.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock

from modules.content_extractor import ContentExtractor, SlideContent


class TestContentExtractor:
    """Test cases for ContentExtractor class."""

    def test_initialization(self, mock_config):
        """Test ContentExtractor initialization."""
        extractor = ContentExtractor()

        assert extractor.min_table_rows == 2
        assert extractor.min_table_cols == 2
        assert extractor.preserve_formatting is True

    def test_extract_slide_content(self, mock_config, mock_slide):
        """Test extracting content from a single slide."""
        extractor = ContentExtractor()

        slide_content = extractor.extract_slide_content(mock_slide, 1)

        assert isinstance(slide_content, SlideContent)
        assert slide_content.slide_number == 1
        assert slide_content.title == "Test Slide"
        assert slide_content.has_content is True

    def test_extract_all_slides(self, mock_config, mock_presentation):
        """Test extracting content from all slides."""
        extractor = ContentExtractor()

        slides = extractor.extract_all_slides(mock_presentation)

        assert len(slides) == 2
        assert all(isinstance(s, SlideContent) for s in slides)

    def test_extract_title(self, mock_config, mock_slide):
        """Test title extraction."""
        extractor = ContentExtractor()

        title = extractor._extract_title(mock_slide)

        assert title == "Test Slide"

    def test_extract_title_no_title(self, mock_config):
        """Test title extraction when no title exists."""
        extractor = ContentExtractor()

        slide_no_title = MagicMock()
        slide_no_title.shapes.title = None

        title = extractor._extract_title(slide_no_title)

        assert title is None

    def test_extract_text(self, mock_config, mock_slide):
        """Test text extraction from slide."""
        extractor = ContentExtractor()

        text_blocks = extractor._extract_text(mock_slide)

        assert isinstance(text_blocks, list)
        assert len(text_blocks) > 0

    def test_extract_tables(self, mock_config, mock_slide):
        """Test table extraction from slide."""
        extractor = ContentExtractor()

        tables, table_texts = extractor._extract_tables(mock_slide)

        assert isinstance(tables, list)
        assert isinstance(table_texts, list)
        assert len(tables) == len(table_texts)

    def test_convert_table_to_dataframe(self, mock_config):
        """Test converting PowerPoint table to DataFrame."""
        extractor = ContentExtractor()

        # Mock table
        mock_table = MagicMock()

        # Mock rows with cells
        mock_row1 = MagicMock()
        mock_row1.cells = [
            MagicMock(text="Segment"),
            MagicMock(text="Rate (%)")
        ]

        mock_row2 = MagicMock()
        mock_row2.cells = [
            MagicMock(text="Commercial"),
            MagicMock(text="2.5")
        ]

        mock_row3 = MagicMock()
        mock_row3.cells = [
            MagicMock(text="Retail"),
            MagicMock(text="3.1")
        ]

        mock_table.rows = [mock_row1, mock_row2, mock_row3]

        df, table_text = extractor._convert_table_to_dataframe(mock_table)

        assert isinstance(df, pd.DataFrame)
        assert len(df) >= 2
        assert len(df.columns) >= 2
        assert isinstance(table_text, str)

    def test_format_table_for_llm(self, mock_config, sample_dataframe):
        """Test formatting DataFrame for LLM."""
        extractor = ContentExtractor()

        formatted = extractor._format_table_for_llm(sample_dataframe)

        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert 'Segment' in formatted or 'Commercial' in formatted

    def test_is_numeric(self, mock_config):
        """Test numeric value detection."""
        extractor = ContentExtractor()

        assert extractor._is_numeric("123") is True
        assert extractor._is_numeric("12.5") is True
        assert extractor._is_numeric("$100") is True
        assert extractor._is_numeric("25%") is True
        assert extractor._is_numeric("1,234.56") is True
        assert extractor._is_numeric("text") is False
        assert extractor._is_numeric("Commercial") is False

    def test_get_slide_summary(self, mock_config, mock_slide_content):
        """Test getting slide summary statistics."""
        extractor = ContentExtractor()

        summary = extractor.get_slide_summary(mock_slide_content)

        assert isinstance(summary, dict)
        assert 'slide_number' in summary
        assert 'has_title' in summary
        assert 'text_blocks' in summary
        assert 'table_count' in summary
        assert 'has_content' in summary
        assert summary['slide_number'] == 1
        assert summary['has_title'] is True
        assert summary['table_count'] == 1

    def test_empty_slide_content(self, mock_config):
        """Test handling of empty slide."""
        extractor = ContentExtractor()

        empty_slide = MagicMock()
        empty_slide.shapes.title = None
        empty_slide.shapes = []

        slide_content = extractor.extract_slide_content(empty_slide, 1)

        assert slide_content.has_content is False
        assert len(slide_content.text_content) == 0
        assert len(slide_content.tables) == 0

    def test_slide_with_multiple_tables(self, mock_config):
        """Test extracting slide with multiple tables."""
        extractor = ContentExtractor()

        # Create mock slide with multiple tables
        slide = MagicMock()
        slide.shapes.title.text = "Multi-Table Slide"

        # Create two table shapes
        table1 = MagicMock()
        table1.has_table = True
        mock_table1 = MagicMock()
        row1 = MagicMock()
        row1.cells = [MagicMock(text="A"), MagicMock(text="B")]
        row2 = MagicMock()
        row2.cells = [MagicMock(text="1"), MagicMock(text="2")]
        row3 = MagicMock()
        row3.cells = [MagicMock(text="3"), MagicMock(text="4")]
        mock_table1.rows = [row1, row2, row3]
        table1.table = mock_table1

        table2 = MagicMock()
        table2.has_table = True
        mock_table2 = MagicMock()
        row1 = MagicMock()
        row1.cells = [MagicMock(text="X"), MagicMock(text="Y")]
        row2 = MagicMock()
        row2.cells = [MagicMock(text="10"), MagicMock(text="20")]
        row3 = MagicMock()
        row3.cells = [MagicMock(text="30"), MagicMock(text="40")]
        mock_table2.rows = [row1, row2, row3]
        table2.table = mock_table2

        slide.shapes = [table1, table2]

        slide_content = extractor.extract_slide_content(slide, 1)

        assert len(slide_content.tables) == 2
        assert len(slide_content.table_texts) == 2
