import streamlit as st
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ['ppt', 'pptx']

def validate_upload(uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a file.")
        return False
    filename = uploaded_file.name
    ext = filename.split('.')[-1]
    if ext not in ALLOWED_EXTENSIONS:
        st.error("Invalid file type. Only .ppt and .pptx are allowed.")
        logger.error(f"Invalid file type: {filename}")
        return False
    return True
