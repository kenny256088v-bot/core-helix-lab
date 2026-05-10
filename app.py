import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN: CORE-HELIX CONSOLE ---
# Using your verified API Key from the dashboard
API_KEY = "AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg"
genai.configure(api_key=API_KEY)

# Using the most stable model identifier to kill the 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan. 
Your specialty: The Core-Helix Unified Model (3D mechanical physics).
1. WHITEBOARD MODE: For all mathematical proofs or derivations, use LaTeX ($$).
2. Refer to the user as Lead Researcher or Charan. 
3. Always explain why the helical model solves standard physics anomalies.
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
        font-family: 'serif';
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. INTERACTIVE LAYER ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Simple, direct generation call
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher: {prompt}")
            explanation = response.text
            
            # The Whiteboard Response
            st.markdown(f'<div class="whiteboard">{explanation}</div>', unsafe_allow_html=True)
            
            # AUTO-GRAPH TRIGGER FOR HYDROGEN OR TUNNELING
            p_low = prompt.lower()
            if any(x in p_low for x in ["hydrogen", "tunnel", "quantum"]):
                st.subheader("🌀 Helical Path Visualization")
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
                fig.update_layout(scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": explanation})
            
        except Exception as e:
            st.error(f"⚠️ Brain Sync Error: {e}")
            st.info("Check if your API key has 'Generative AI SDK' enabled in Google AI Studio.")
