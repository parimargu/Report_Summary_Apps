"""
Main Streamlit application for PowerPoint Content Summarization.

This is the entry point for the application.
"""

import sys
from pathlib import Path

import streamlit as st

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.logger import LoggerManager, get_logger
from modules.config_manager import get_config
from modules.file_parser import FileParser
from modules.content_extractor import ContentExtractor
from modules.llm_service import LLMService
from modules.ui_renderer import UIRenderer


# Initialize components
@st.cache_resource
def initialize_app():
    """Initialize application components (cached)."""
    try:
        # Load configuration
        config = get_config()

        # Setup logging
        log_manager = LoggerManager()
        log_manager.setup_logger(
            name='ppt_summarizer',
            log_level=config.get('logging.level', 'INFO'),
            log_file=config.get('logging.file', 'app.log'),
            console_output=config.get('logging.console_output', True),
            file_output=config.get('logging.file_output', True),
            max_bytes=config.get('logging.max_bytes', 10485760),
            backup_count=config.get('logging.backup_count', 5)
        )

        logger = get_logger(__name__)
        logger.info("=" * 80)
        logger.info("Starting PowerPoint Content Summarization Application")
        logger.info("=" * 80)

        # Initialize services
        parser = FileParser()
        extractor = ContentExtractor()
        llm_service = LLMService()
        ui_renderer = UIRenderer()

        # Test LLM connection
        if not llm_service.test_connection():
            logger.error("Failed to connect to Groq API")
            st.error("⚠️ Failed to connect to Groq API. Please check your API key.")
            return None

        logger.info("All components initialized successfully")

        return {
            'config': config,
            'parser': parser,
            'extractor': extractor,
            'llm': llm_service,
            'ui': ui_renderer,
            'logger': logger
        }

    except Exception as e:
        st.error(f"❌ Failed to initialize application: {str(e)}")
        st.exception(e)
        return None


def configure_page():
    """Configure Streamlit page settings."""
    config = get_config()

    st.set_page_config(
        page_title=config.get('ui.page_title', 'PowerPoint Summarizer'),
        page_icon=config.get('ui.page_icon', '📊'),
        layout=config.get('ui.layout', 'wide'),
        initial_sidebar_state=config.get('ui.sidebar_state', 'expanded')
    )


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    if 'slides_data' not in st.session_state:
        st.session_state.slides_data = None

    if 'presentation_loaded' not in st.session_state:
        st.session_state.presentation_loaded = False

    if 'active_summary_table' not in st.session_state:
        st.session_state.active_summary_table = None


def process_uploaded_file(uploaded_file, components):
    """
    Process uploaded PowerPoint file.

    Args:
        uploaded_file: Streamlit uploaded file object
        components: Dictionary of initialized components
    """
    parser = components['parser']
    extractor = components['extractor']
    logger = components['logger']

    try:
        logger.info(f"Processing uploaded file: {uploaded_file.name}")

        with st.spinner("🔍 Parsing presentation..."):
            # Parse presentation
            presentation = parser.parse_uploaded_presentation(uploaded_file)

            # Extract content from all slides
            slides_data = extractor.extract_all_slides(presentation)

            # Store in session state
            st.session_state.slides_data = slides_data
            st.session_state.presentation_loaded = True
            st.session_state.current_slide = 0

            logger.info(f"Successfully processed {len(slides_data)} slides")

        st.success(f"✅ Successfully loaded presentation with {len(slides_data)} slides!")

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        st.error(f"❌ Error processing file: {str(e)}")
        st.session_state.presentation_loaded = False


def generate_table_summary(slide_number, table_index, table_text, components):
    """
    Generate AI summary for a table.

    Args:
        slide_number: Slide number
        table_index: Table index on the slide
        table_text: Formatted table text
        components: Dictionary of initialized components
    """
    llm_service = components['llm']
    logger = components['logger']

    summary_key = f'summary_{slide_number}_{table_index}'

    try:
        logger.info(f"Generating summary for slide {slide_number}, table {table_index}")

        with st.spinner("🤖 Generating AI summary..."):
            summary = llm_service.generate_summary(table_text)

            if summary:
                st.session_state[summary_key] = summary
                # Clear the generate flag after successful generation
                st.session_state[f'generate_{slide_number}_{table_index}'] = False
                logger.info("Summary generated successfully")
                # Force rerun to display the summary
                st.rerun()
            else:
                st.error("Failed to generate summary")
                logger.error("LLM returned empty summary")

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}", exc_info=True)
        st.error(f"❌ Error generating summary: {str(e)}")


def main():
    """Main application function."""
    # Configure page
    configure_page()

    # Initialize session state
    initialize_session_state()

    # Initialize components
    components = initialize_app()

    if components is None:
        st.stop()
        return

    ui_renderer = components['ui']
    logger = components['logger']

    # Render UI
    ui_renderer.render_header()
    ui_renderer.render_sidebar_info()

    # File upload section
    uploaded_file = ui_renderer.render_file_uploader()

    if uploaded_file is not None:
        # Check if we need to process the file
        if not st.session_state.presentation_loaded or \
           st.session_state.get('last_uploaded_file') != uploaded_file.name:

            st.session_state.last_uploaded_file = uploaded_file.name
            process_uploaded_file(uploaded_file, components)

    # Display presentation content if loaded
    if st.session_state.presentation_loaded and st.session_state.slides_data:
        slides_data = st.session_state.slides_data

        st.markdown("---")

        # Show statistics
        ui_renderer.render_statistics(slides_data)

        st.markdown("---")

        # Slide navigation
        current_slide_idx = ui_renderer.render_slide_navigation(len(slides_data))

        st.markdown("---")

        # Display current slide
        current_slide = slides_data[current_slide_idx]

        if not current_slide.has_content:
            st.warning("⚠️ This slide appears to be empty or contains no extractable content.")
        else:
            # Check if we need to generate summaries BEFORE rendering
            for table_idx in range(1, len(current_slide.tables) + 1):
                generate_key = f'generate_{current_slide.slide_number}_{table_idx}'

                if st.session_state.get(generate_key, False):
                    # Generate summary
                    table_text = current_slide.table_texts[table_idx - 1]
                    generate_table_summary(
                        current_slide.slide_number,
                        table_idx,
                        table_text,
                        components
                    )
                    # The generate_table_summary function now handles rerun
                    return  # Exit early to trigger rerun

            # Render slide content (this will now show summaries if they exist)
            ui_renderer.render_slide_content(current_slide)

    else:
        # Show instructions when no file is uploaded
        st.info(
            """
            👆 **Get Started:**
            1. Upload a PowerPoint presentation (.ppt or .pptx) using the file uploader above
            2. The application will automatically extract text and tables from each slide
            3. Navigate through slides and click "Generate AI Summary" to analyze table data
            4. Get instant AI-powered insights highlighting key financial metrics and risk indicators
            """
        )

        # Show sample data info
        st.markdown("---")
        st.markdown("### 📋 Sample Data")
        st.info(
            """
            Don't have a presentation? You can use our sample file located at:
            `sample_data/sample_loan_forecast.pptx`
            
            This sample contains quarterly loan forecasting data with:
            - Multiple slides with text descriptions
            - Tables showing Loan Default Rate (%) and Net Rate (%)
            - Various banking segments (Commercial, Retail, Mortgage)
            """
        )

    logger.debug("Main application loop completed")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application error: {str(e)}")
        st.exception(e)
