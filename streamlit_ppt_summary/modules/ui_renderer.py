import streamlit as st
import asyncio
import logging

logger = logging.getLogger(__name__)


def render_slide(slide_content, llm_summarizer, prompt_template):
    cols = st.columns([1, 1])
    with cols[0]:
        st.subheader("Paragraphs")
        for para in slide_content['paragraphs']:
            st.write(para)

    with cols[1]:
        st.subheader("Tables")
        summaries = []
        for table_df in slide_content['tables']:
            st.dataframe(table_df)
            if st.button("Generate Table Summary", key=id(table_df)):
                summary = asyncio.run(
                    llm_summarizer.summarize_table(table_df, prompt_template)
                )
                #st.markdown(f"**Summary:**\n- {summary.replace('\n', '\n- ')}")
                # Replace newlines with markdown bullets
                formatted_summary = summary.replace("\n", "\n- ")
                st.markdown(f"**Summary:**\n- {formatted_summary}")

