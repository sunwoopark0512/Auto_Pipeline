import streamlit as st
from pipeline_orchestrator import run_pipeline

st.set_page_config(page_title="Content Automation Dashboard", layout="centered")

st.title("\U0001F680 Content Automation Pipeline")

topic = st.text_input("Enter Topic", value="AI in Marketing")
token = st.text_input("Enter WordPress API Token", type="password")

if st.button("Run Pipeline"):
    if topic and token:
        st.write("\u2699\ufe0f Running pipeline...")
        run_pipeline(topic, token)
        st.success("\u2705 Pipeline completed successfully!")
    else:
        st.warning("Please fill both Topic and API Token.")
