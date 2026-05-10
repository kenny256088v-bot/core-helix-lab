import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions # Added for version control
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN: CORE-HELIX INTELLIGENCE ---
# Using your verified API Key
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# FORCE API v1: This prevents the 404/NotFound errors seen in your screenshots
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    request_options=RequestOptions(api_version='v1')
)

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan at IIIT Kurnool.
Your mission is to defend and explain the 'Core-Helix Unified Model'.
1. WHITEBOARD MODE: When explaining derivations (like Quantum Tunneling), use LaTeX ($$) formatting.
2. MECHANICAL TRUTH: Explain why things happen in 3D (helical pitch) rather than 1D (standard strings).
3. Be professional, technical, and always refer to the user as Lead Researcher or Charan.
4. If asked about Mountain 1-5, explain the mechanical 'gears' and trigger a graph.
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
        font-family: 'Georgia', serif;
        box-shadow: 0 4px 15px rgba(0,242,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LAB PARTNER: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. AUTOMATIC GRAPH TRIGGERS ---
def plot_mountain_5():
    st.info("📊 Rendering Mountain 5 Thermal Data...")
    x = np.linspace(1700, 1900, 100)
    y = np.where(x > 1808, 15, 0)
    fig = go.Figure(data=[go.Scatter(x=x, y=y, line=dict(color='#00f2ff', width=4))])
    fig.update_layout(title="Iron-56 Pitch-Slip Anomaly (1808K)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def plot_tunneling():
    st.info("🌀 Visualizing Helical Threading...")
    t = np.linspace(0, 10, 500)
    fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*8), y=np.cos(t*8), z=t, mode='lines', line=dict(color='#7000ff', width=8))])
    fig.update_layout(title="Quantum Tunneling: 3D Spiral Migration", scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE INTERACTION LAYER ---
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
            full_query = f"{SYSTEM_PROMPT}\n\nResearcher Input: {prompt}"
            response = model.generate_content(full_query)
            
            # The Whiteboard Response
            st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
            
            # Auto-Graphics
            p_low = prompt.lower()
            if any(x in p_low for x in ["iron", "56", "mountain 5", "heat"]):
                plot_mountain_5()
            if any(x in p_low for x in ["tunnel", "quantum", "barrier"]):
                plot_tunneling()
                
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ Brain Sync Failure: {e}")
            st.write("Check if the Gemini API is active for your region or if the key has been restricted.")
