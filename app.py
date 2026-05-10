import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. CORE-HELIX HARDWARE SYNC ---
# Using your verified key from the fresh project
genai.configure(api_key="AIzaSyBpiMFLtK7z6igFL_xeK0coQGQiL6eg00E")

# We target the model name directly. 
# Removing the 'models/' prefix prevents the v1beta redirection.
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan. 
Specialty: Core-Helix Unified Model (3D mechanical physics).
1. WHITEBOARD MODE: Use LaTeX ($$) for physics derivations.
2. MECHANICAL TRUTH: Space is 3D helical mechanics.
3. Be professional and highly technical.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM UI ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #0e1117;
        border-left: 10px solid #00f2ff;
        padding: 30px;
        border-radius: 12px;
        color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. INTERACTIVE LAYER ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Forcing stable execution
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher: {prompt}")
            
            # Whiteboard Response
            st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
            
            # 3D HELIX VISUALIZATION
            if any(x in prompt.lower() for x in ["hydrogen", "helical", "rotation"]):
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
                fig.update_layout(title="Helical Path Projection", scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # We trap the error without exposing the key in logs
            st.error(f"⚠️ Brain Sync Jitter: {e}")
            st.info("Check if the 'Generative Language API' is enabled in your Google Cloud Library.")
            
