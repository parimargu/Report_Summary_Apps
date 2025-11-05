"""
UI rendering module for Streamlit interface.

Provides reusable UI components and layout functions.
"""

from typing import List, Optional
import pandas as pd
import streamlit as st

from modules.logger import get_logger
from modules.content_extractor import SlideContent

logger = get_logger(__name__)


class UIRenderer:
    """Handles rendering of Streamlit UI components."""

    def __init__(self):
        """Initialize UI renderer."""
        logger.info("UIRenderer initialized")

    @staticmethod
    def render_header():
        """Render application header."""
        st.title("📊 PowerPoint Content Summarization")
        st.markdown(
            """
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='margin: 0; color: #1f77b4;'>AI-Powered Financial Report Analysis</h3>
                <p style='margin: 5px 0 0 0; color: #555;'>
                    Upload PowerPoint presentations containing loan forecasts and get instant AI-generated summaries 
                    of your table data highlighting key metrics and risk indicators.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def render_file_uploader() -> Optional[any]:
        """
        Render file upload component.

        Returns:
            Uploaded file object or None
        """
        st.subheader("📁 Upload Presentation")

        uploaded_file = st.file_uploader(
            "Choose a PowerPoint file (.ppt or .pptx)",
            type=['ppt', 'pptx'],
            help="Maximum file size: 5MB"
        )

        return uploaded_file

    @staticmethod
    def render_slide_navigation(total_slides: int) -> int:
        """
        Render slide navigation controls.

        Args:
            total_slides: Total number of slides

        Returns:
            Selected slide number (0-indexed)
        """
        st.subheader("🎯 Slide Navigation")

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.get('current_slide', 0) <= 0):
                st.session_state.current_slide = max(0, st.session_state.current_slide - 1)
                st.rerun()

        with col2:
            current_slide = st.selectbox(
                "Select Slide",
                range(total_slides),
                format_func=lambda x: f"Slide {x + 1} of {total_slides}",
                key='slide_selector',
                index=st.session_state.get('current_slide', 0)
            )
            st.session_state.current_slide = current_slide

        with col3:
            if st.button("Next ➡️", disabled=st.session_state.get('current_slide', 0) >= total_slides - 1):
                st.session_state.current_slide = min(total_slides - 1, st.session_state.current_slide + 1)
                st.rerun()

        return current_slide

    @staticmethod
    def render_slide_content(slide_content: SlideContent):
        """
        Render slide content in two-column layout.

        Args:
            slide_content: SlideContent object containing extracted data
        """
        # Display slide title
        if slide_content.title:
            st.markdown(f"### 📄 {slide_content.title}")
        else:
            st.markdown(f"### 📄 Slide {slide_content.slide_number}")

        st.markdown("---")

        # Two-column layout
        left_col, right_col = st.columns([1, 1], gap="large")

        # Left panel: Text content
        with left_col:
            st.markdown("#### 📝 Text Content")

            if slide_content.text_content:
                for idx, text in enumerate(slide_content.text_content, 1):
                    with st.container():
                        st.markdown(
                            f"""
                            <div style='background-color: #f8f9fa; padding: 15px; 
                                        border-radius: 8px; margin-bottom: 10px; 
                                        border-left: 4px solid #1f77b4;'>
                                {text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("No text content found on this slide.")

        # Right panel: Tables
        with right_col:
            st.markdown("#### 📊 Table Data")

            if slide_content.tables:
                for idx, (df, table_text) in enumerate(
                    zip(slide_content.tables, slide_content.table_texts), 1
                ):
                    with st.expander(f"Table {idx}", expanded=True):
                        # Display table
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                        # Generate summary button
                        button_key = f"generate_summary_{slide_content.slide_number}_{idx}"
                        if st.button(
                            "🤖 Generate AI Summary",
                            key=button_key,
                            type="primary",
                            use_container_width=True
                        ):
                            st.session_state[f'generate_{slide_content.slide_number}_{idx}'] = True
                            st.session_state[f'active_summary_table'] = idx
                            st.rerun()
            else:
                st.info("No tables found on this slide.")

        # Bottom section: AI-Generated Summary (Full Width)
        st.markdown("---")

        # Check if any summary exists for this slide
        has_summary = False
        active_summary_idx = None

        for idx in range(1, len(slide_content.tables) + 1):
            summary_key = f'summary_{slide_content.slide_number}_{idx}'
            if summary_key in st.session_state:
                has_summary = True
                active_summary_idx = idx
                break

        if has_summary and active_summary_idx:
            summary_key = f'summary_{slide_content.slide_number}_{active_summary_idx}'

            st.markdown("### 💡 AI-Generated Summary")
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%); 
                            padding: 25px; 
                            border-radius: 12px; 
                            border: 2px solid #28a745;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin-bottom: 20px;'>
                    <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                        <span style='font-size: 24px; margin-right: 10px;'>🤖</span>
                        <span style='font-weight: bold; font-size: 18px; color: #2c3e50;'>
                            Analysis for Table {active_summary_idx}
                        </span>
                    </div>
                    <div style='background-color: white; 
                                padding: 20px; 
                                border-radius: 8px;
                                font-size: 15px;
                                line-height: 1.8;
                                color: #333;
                                white-space: pre-wrap;
                                border-left: 4px solid #28a745;'>
                        {st.session_state[summary_key]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Add a clear button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ Clear Summary", use_container_width=True):
                    del st.session_state[summary_key]
                    if 'active_summary_table' in st.session_state:
                        del st.session_state['active_summary_table']
                    st.rerun()

    @staticmethod
    def render_processing_status(message: str, status_type: str = "info"):
        """
        Render processing status message.

        Args:
            message: Status message
            status_type: Type of status (info, success, warning, error)
        """
        if status_type == "info":
            st.info(message)
        elif status_type == "success":
            st.success(message)
        elif status_type == "warning":
            st.warning(message)
        elif status_type == "error":
            st.error(message)

    @staticmethod
    def render_statistics(slides: List[SlideContent]):
        """
        Render presentation statistics.

        Args:
            slides: List of SlideContent objects
        """
        st.subheader("📈 Presentation Statistics")

        total_slides = len(slides)
        slides_with_text = sum(1 for s in slides if s.text_content)
        slides_with_tables = sum(1 for s in slides if s.tables)
        total_tables = sum(len(s.tables) for s in slides)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Slides", total_slides)

        with col2:
            st.metric("Slides with Text", slides_with_text)

        with col3:
            st.metric("Slides with Tables", slides_with_tables)

        with col4:
            st.metric("Total Tables", total_tables)

    @staticmethod
    def render_error(error_message: str):
        """
        Render error message.

        Args:
            error_message: Error message to display
        """
        st.error(f"❌ Error: {error_message}")
        logger.error(f"UI Error displayed: {error_message}")

    @staticmethod
    def render_loading_spinner(message: str = "Processing..."):
        """
        Render loading spinner.

        Args:
            message: Loading message

        Returns:
            Spinner context manager
        """
        return st.spinner(message)

    @staticmethod
    def render_sidebar_info():
        """Render sidebar information."""
        with st.sidebar:
            st.markdown("### ℹ️ About")
            st.markdown(
                """
                This application uses AI to analyze PowerPoint presentations 
                containing financial forecasts and loan prediction data.
                
                **Key Features:**
                - 📤 Upload .ppt or .pptx files
                - 📊 Automatic table extraction
                - 🤖 AI-powered summaries
                - 🎯 Focus on risk indicators
                
                **Metrics Analyzed:**
                - Loan Default Rate (%)
                - Net Rate (%)
                - Negative values
                - Abnormal trends
                """
            )

            st.markdown("---")
            st.markdown("### 🔧 Settings")
            st.info("Configuration loaded from config.yaml")

            st.markdown("---")
            st.markdown(
                """
                <div style='text-align: center; color: #888; font-size: 0.8em;'>
                    Powered by Groq LLM<br>
                    Version 1.0.0
                </div>
                """,
                unsafe_allow_html=True
            )


# Example usage
if __name__ == "__main__":
    renderer = UIRenderer()

    # This would normally be in the main Streamlit app
    renderer.render_header()
    renderer.render_sidebar_info()
