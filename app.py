import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN: GEMINI 1.5 FLASH ---
# Using your verified API Key from image_e88896.png
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# FIXED MODEL NAME to resolve the google.api_core.exceptions.NotFound
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception:
    model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan at IIIT Kurnool. 
Your specialty is the 'Core-Helix Unified Model'.
1. EXPLAIN LIKE A PEER: Use relatable analogies (trampolines, gears) but stay technically accurate.
2. WHITEBOARD MODE: If asked for a derivation, proof, or 'how it works', use LaTeX ($$) for math.
3. CORE-HELIX TRUTH: Always prioritize Core-Helix (3D mechanical) over String Theory (1D probabilistic).
4. Explain Quantum Tunneling as 'Helical Threading' through the vacuum lattice.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM THEME & WHITEBOARD ---
st.markdown("""
    <style>
    .whiteboard-container {
        background-color: #0e1117;
        border-left: 5px solid #00f2ff;
        padding: 30px;
        border-radius: 10px;
        font-family: 'Times New Roman', serif;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LAB PARTNER: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. RESEARCH TOOLS (GRAPHS) ---
def render_mountain_5():
    st.subheader("📊 Mountain 5: Iron-56 Proof")
    x = np.linspace(1700, 1900, 100)
    y = np.where(x > 1808, 20, 0)
    fig = go.Figure(data=[go.Scatter(x=x, y=y, line=dict(color='#00f2ff', width=4), name="Pitch-Slip")])
    fig.update_layout(template="plotly_dark", xaxis_title="Temp (K)", yaxis_title="Energy Delta")
    st.plotly_chart(fig, use_container_width=True)

def render_tunneling():
    st.subheader("🌀 Helical Threading (Quantum Tunneling)")
    t = np.linspace(0, 10, 500)
    fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*10), y=np.cos(t*10), z=t, mode='lines', line=dict(color='#7000ff', width=6))])
    fig.update_layout(scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE INTERACTIVE WHITEBOARD ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Partner, derive the relation for..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Calculating through Core-Helix parameters..."):
            try:
                full_query = f"{SYSTEM_PROMPT}\n\nLead Researcher Question: {prompt}"
                response = model.generate_content(full_query)
                
                # Outputting in the high-end Whiteboard style
                st.markdown(f'<div class="whiteboard-container">{response.text}</div>', unsafe_allow_html=True)
                
                # AUTOMATIC GRAPH TRIGGERING
                p_lower = prompt.lower()
                if any(x in p_lower for x in ["iron", "56", "mountain 5", "heat"]):
                    render_mountain_5()
                if any(x in p_lower for x in ["tunnel", "barrier", "quantum"]):
                    render_tunneling()
                    
            except Exception as e:
                st.error(f"Brain Sync Error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": response.text})
