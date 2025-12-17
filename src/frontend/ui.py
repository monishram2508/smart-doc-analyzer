import streamlit as st
import sys
import os
from pathlib import Path
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- PATH SETUP ---
current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent.parent
sys.path.append(str(project_root))

from src.backend.loader import get_query_engine

# --- PAGE CONFIG (Tab Title & Icon) ---
st.set_page_config(
    page_title="DocQuery",
    page_icon="⚖️",
    layout="wide"  # Uses the full screen width
)

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.title("Document Control")
    st.info("System Status: **Online**")
    
    st.divider()
    
    st.subheader("Model Configuration")
    model_choice = st.selectbox("Select Model", ["GPT-4o-mini (Fast)", "GPT-4o (Precise)"])
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.2)
    
    st.divider()
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN PAGE ---
st.title("DocQuery")
st.caption("Powered by Streamlit & ChromaDB")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am ready to analyze your legal documents. What would you like to know?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about the documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            try:
                engine = get_query_engine()
                response = engine.query(prompt) 
                
                st.markdown(str(response))
                st.session_state.messages.append({"role": "assistant", "content": str(response)})
            except Exception as e:
                st.error(f"Error: {e}")