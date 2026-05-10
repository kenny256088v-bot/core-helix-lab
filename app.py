import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
from gtts import gTTS # Fixed the ModuleNotFoundError
import base64

# --- 1. RESEARCHER CONFIG ---
# Using your verified API Key
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# Reverted to most stable model name to fix 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan. 
Explain the 'Core-Helix Unified Model' with technical precision.
1. WHITEBOARD: Use LaTeX ($$) for physics derivations.
2. MECHANICAL TRUTH: Space is a 3D helical structure, not 1D strings.
3. Be supportive and refer to the user as Lead Researcher or Charan.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM WHITEBOARD UI ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #0e1117;
        border-left: 10px solid #00f2ff;
        padding: 25px;
        border-radius: 12px;
        color: #f0f0f0;
        font-family: 'serif';
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. CHAT & AUDIO LOGIC ---
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
            # Generate Physics Response
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher Input: {prompt}")
            text_out = response.text
            
            # Display on Whiteboard
            st.markdown(f'<div class="whiteboard">{text_out}</div>', unsafe_allow_html=True)
            
            # --- THE ORACLE'S VOICE (gTTS) ---
            tts = gTTS(text=text_out[:300], lang='en') # Audio for the first 300 chars
            tts.save("response.mp3")
            with open("response.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": text_out})
            
        except Exception as e:
            st.error(f"⚠️ Brain Sync Failure: {e}")
