import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
from gtts import gTTS
import base64
import io

# --- 1. STABLE BRAIN CONFIGURATION ---
# Using verified key from your dashboard
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# We use the most direct model call to avoid v1beta 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan. 
Expertise: Core-Helix Unified Model.
1. WHITEBOARD: Use LaTeX ($$) for all physics derivations.
2. MECHANICAL TRUTH: Explain space as 3D helical mechanics, not 1D probability.
3. Be technical, professional, and refer to the user as Lead Researcher.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM WHITEBOARD UI ---
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

# --- 2. THE INTERACTIVE WHITEBOARD ---
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.chat_log.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate the physics explanation
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nQuestion: {prompt}")
            
            # Display in Whiteboard style
            st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
            
            # --- THE ORACLE'S VOICE (gTTS) ---
            # Fixed the ModuleNotFoundError from image_e98f08
            tts = gTTS(text=response.text[:300], lang='en')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            b64_audio = base64.b64encode(audio_io.read()).decode()
            st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>', unsafe_allow_html=True)

            st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            
            # AUTO-GRAPH FOR HYDROGEN
            if "hydrogen" in prompt.lower():
                st.subheader("🌀 Hydrogen Helical Structure")
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=5))])
                fig.update_layout(scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Brain Sync Error: {e}")
            st.info("If 404 persists, ensure your Google Cloud Project has the Gemini API enabled for the 'v1' stable path.")
