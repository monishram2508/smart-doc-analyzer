import streamlit as st
import sys
import requests
from pathlib import Path
from streamlit_lottie import st_lottie

current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent.parent
sys.path.append(str(project_root))

from src.backend.loader import get_query_engine

st.set_page_config(
    page_title="DocQuery (Offline)",
    page_icon="🛡️",
    layout="wide"
)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_secure = load_lottieurl("https://lottie.host/98a7a9cb-472e-4621-89eb-23dfdfb5821c/v6j4Wjk6wZ.json")

with st.sidebar:
    if lottie_secure:
        st_lottie(lottie_secure, height=150, key="secure_anim")
    
    st.title("Secure Mode")
    st.success("System Status: **Offline (Air-Gapped)**")
    
    st.divider()
    
    st.subheader("Model Info")
    st.code("Model: Llama 3.2\nType: Local LLM\nPrivacy: 100%", language="yaml")
    
    st.divider()
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

st.title("DocQuery: Sovereign AI")
st.caption("Analyzing documents locally. No data leaves this device.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I am ready. Your documents are loaded securely. What do you need?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        with st.status("Activating AI Brain", expanded=True) as status:
            try:
                st.write("Connecting to Local Database")
                engine = get_query_engine()
                
                st.write("Reading Documents...")
                streaming_response = engine.query(prompt)
                
                status.update(label="Found answer. Generating text.", state="complete", expanded=False)
                
                for token in streaming_response.response_gen:
                    full_response += token
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                status.update(label="Error", state="error")
                st.error(f"Error: {e}")