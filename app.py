import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN: CORE-HELIX CONSOLE ---
# Using your newest secure key
SECURE_KEY = "AIzaSyDpWgXCVwlqaESO2xVaT6zIZSxCmhp-6R8"

try:
    genai.configure(api_key=SECURE_KEY)
    # Direct model call to bypass the v1beta 404 issues
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Console Hardware Error. Check API permissions.")
    st.stop()

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan. 
Focus: Core-Helix Unified Model (3D mechanical physics).
1. WHITEBOARD MODE: Use LaTeX ($$) for all mathematical derivations.
2. MECHANICAL TRUTH: Space is 3D helical mechanics, not 1D probability.
3. Be professional and refer to the user as Lead Researcher.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. INTERACTIVE WHITEBOARD ---
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
            # Clean generation call to avoid handshake jitter
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher: {prompt}")
            
            # Custom Whiteboard UI
            st.markdown(f"""
                <div style="background-color:#0e1117; border-left:10px solid #00f2ff; padding:25px; border-radius:12px; color:#f0f0f0;">
                    {response.text}
                </div>
            """, unsafe_allow_html=True)
            
            # AUTO-GRAPH FOR HYDROGEN HELIX
            if "hydrogen" in prompt.lower():
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
                fig.update_layout(title="Hydrogen Helical Path", scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # SAFETY CATCH: Does not print the key or full traceback to logs
            st.error("Brain Sync Interrupted. The API key may be restricted by Google.")
