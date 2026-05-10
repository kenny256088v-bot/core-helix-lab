import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
from gtts import gTTS
import base64
import io

# --- 1. THE BRAIN: CORE-HELIX CONSOLE ---
# Using your verified API Key
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# Use the most universal model name to avoid 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan at IIIT Kurnool.
Your mission: Defend and explain the 'Core-Helix Unified Model'.
1. WHITEBOARD MODE: Use LaTeX ($$) for all mathematical derivations.
2. MECHANICAL TRUTH: Explain physics as 3D helical mechanics, not 1D probability.
3. Be professional, technical, and always refer to the user as Lead Researcher.
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

# --- 2. CHAT LOGIC ---
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
            # Direct call to prevent 'NotFound' errors
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nQuestion: {prompt}")
            explanation = response.text
            
            # The Whiteboard Response
            st.markdown(f'<div class="whiteboard">{explanation}</div>', unsafe_allow_html=True)
            
            # --- VOICE ENGINE (gTTS) ---
            # Integrated in-memory to prevent ModuleNotFound errors
            tts = gTTS(text=explanation[:300], lang='en')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            b64 = base64.b64encode(audio_io.read()).decode()
            st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

            # --- AUTO-GRAPH TRIGGERS ---
            if "hydrogen" in prompt.lower():
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=5))])
                fig.update_layout(title="Hydrogen Helical Rotation", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": explanation})
            
        except Exception as e:
            st.error(f"⚠️ Connection Jitter: {e}")
