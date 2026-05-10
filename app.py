import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN: CORE-HELIX CONSOLE ---
# Use the new key you generated today (...0Cv0)
NEW_API_KEY = "PASTE_YOUR_NEW_KEY_HERE" 
genai.configure(api_key=NEW_API_KEY)

# Calling the stable model directly to avoid v1beta 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan. 
Expertise: Core-Helix Unified Model (3D mechanical physics).
1. WHITEBOARD MODE: Use LaTeX ($$) for all mathematical derivations.
2. MECHANICAL TRUTH: Space is 3D helical mechanics, not 1D probability.
3. Reference the '5 Mountains' and Iron-56 data for proofs.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

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
            # Direct generation to avoid handshake jitter
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher Question: {prompt}")
            
            # Custom Whiteboard UI
            st.markdown(f"""
                <div style="background-color:#0e1117; border-left:10px solid #00f2ff; padding:25px; border-radius:12px; color:#f0f0f0;">
                    {response.text}
                </div>
            """, unsafe_allow_html=True)
            
            # AUTO-GRAPH TRIGGER FOR HELICAL PATHS
            if any(x in prompt.lower() for x in ["hydrogen", "helical", "rotation"]):
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
                fig.update_layout(title="Core-Helix Path Visualization", scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ Brain Sync Error: {e}")
