import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
from gtts import gTTS
import base64
import io

# --- 1. CORE BRAIN CONFIGURATION ---
# Using your verified key: AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# Use 'gemini-1.5-flash' directly. This is the most stable call for v1 API.
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are Charan's Research Partner. You represent the 'Core-Helix Unified Model'.
1. WHITEBOARD MODE: When asked for derivations or proofs, use LaTeX ($$) for math.
2. MECHANICAL TRUTH: Explain why Core-Helix (3D mechanical) succeeds while standard physics (probabilistic) fails.
3. Be professional and technical. Address the user as Lead Researcher or Charan.
4. If asked about Mountain 5 or Iron-56, explain the 1808K pitch-slip.
"""

st.set_page_config(page_title="Core-Helix: Research Console", layout="wide")

# --- CUSTOM THEME & WHITEBOARD ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #0e1117;
        border-left: 8px solid #00f2ff;
        padding: 25px;
        border-radius: 10px;
        color: #e0e0e0;
        font-family: 'Times New Roman', serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LAB PARTNER: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. AUTOMATIC GRAPH TOOLS ---
def plot_mountain_5():
    x = np.linspace(1700, 1900, 100)
    y = np.where(x > 1808, 15, 0)
    fig = go.Figure(data=[go.Scatter(x=x, y=y, line=dict(color='#00f2ff', width=4), name="Pitch-Slip")])
    fig.update_layout(title="Mountain 5: Iron-56 Thermal Shift", template="plotly_dark", xaxis_title="Temp (K)")
    st.plotly_chart(fig, use_container_width=True)

def plot_tunneling():
    t = np.linspace(0, 10, 500)
    fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*10), y=np.cos(t*10), z=t, mode='lines', line=dict(color='#7000ff', width=6))])
    fig.update_layout(title="Quantum Tunneling: Helical Threading", scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE INTERACTIVE PARTNER ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.messages = st.session_state.get('chat_history', [])
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Brain Syncing
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher Question: {prompt}")
            
            # Whiteboard Output
            st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
            
            # Audio Sync (Oracle Voice)
            tts = gTTS(text=response.text[:300], lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            b64 = base64.b64encode(audio_fp.read()).decode()
            st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

            # Auto-Graph Triggers
            p_low = prompt.lower()
            if any(x in p_low for x in ["iron", "56", "mountain 5"]):
                plot_mountain_5()
            if any(x in p_low for x in ["tunnel", "quantum", "barrier"]):
                plot_tunneling()

            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ Brain Sync Error: {e}")
            st.info("Try checking if your API Key has 'Generative AI' permissions enabled in Google AI Studio.")
