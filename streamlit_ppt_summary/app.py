import streamlit as st
import logging
from modules import file_handler, ppt_parser, llm_handler, ui_renderer, config_manager

# ---------------- Logging ----------------
config = config_manager.load_config()
logging.basicConfig(
    filename=config['logging']['file'],
    level=getattr(logging, config['logging']['level']),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------- App UI ----------------
st.title(config['app']['name'])

uploaded_file = st.file_uploader("Upload PowerPoint File", type=["ppt","pptx"])
if file_handler.validate_upload(uploaded_file):
    slides_content = ppt_parser.parse_ppt(uploaded_file)

    api_key = config_manager.get_env_var(config['llm']['api_key_env_var'])
    if not api_key:
        st.error("GROQ_API_KEY not set in environment variables.")
    else:
        llm_summarizer = llm_handler.LLMSummarizer(
            model_name=config['llm']['model'],
            api_key=api_key,
            timeout=config['llm']['timeout'],
            retries=config['llm']['retry_attempts']
        )

        prompt_template = open('prompt_template.txt', 'r').read()
        for idx, slide in enumerate(slides_content):
            st.markdown(f"---\n### Slide {idx+1}")
            ui_renderer.render_slide(slide, llm_summarizer, prompt_template)
