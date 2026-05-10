import os
import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# =========================================
# CORE-HELIX RESEARCH CONSOLE
# =========================================

st.set_page_config(
    page_title="Core-Helix Research Console",
    layout="wide"
)

# =========================================
# API SETUP
# =========================================

# Store API key in Streamlit secrets or environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Missing Gemini API Key.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================================
# SYSTEM PROMPT
# =========================================

SYSTEM_PROMPT = """
You are the official Lab Partner for Lead Researcher Charan at IIIT Kurnool.

Your mission is to defend and explain the Core-Helix Unified Model.

Rules:
1. Use LaTeX formatting when deriving equations.
2. Explain physical mechanisms in 3D spiral/helical geometry.
3. Maintain technical and professional tone.
4. Refer to the user as Lead Researcher or Charan.
"""

# =========================================
# CUSTOM STYLING
# =========================================

st.markdown("""
<style>
.main-title {
    color: #00f2ff;
    font-size: 42px;
    font-weight: bold;
}

.status {
    color: #00f2ff;
    font-weight: bold;
    margin-bottom: 20px;
}

.response-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #00f2ff;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.markdown('<div class="main-title">⚛️ CORE-HELIX RESEARCH CONSOLE</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="status">LAB PARTNER: ACTIVE | LEAD RESEARCHER: CHARAN</div>',
    unsafe_allow_html=True
)

# =========================================
# SESSION MEMORY
# =========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# DISPLAY HISTORY
# =========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================
# USER INPUT
# =========================================

prompt = st.chat_input("Partner, explain the derivation for...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            full_query = f"""
{SYSTEM_PROMPT}

Researcher Input:
{prompt}
"""

            response = model.generate_content(full_query)

            response_text = response.text

            st.markdown(
                f'<div class="response-box">{response_text}</div>',
                unsafe_allow_html=True
            )

            # =========================================
            # AUTO VISUALIZATION ENGINE
            # =========================================

            p_low = prompt.lower()

            # Iron-56 Graph
            if any(x in p_low for x in ["iron", "56", "mountain 5"]):

                x = np.linspace(1700, 1900, 200)

                y = np.where(x > 1808, 15, 0)

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=y,
                        mode="lines",
                        line=dict(width=4)
                    )
                )

                fig.update_layout(
                    title="Iron-56 Pitch-Slip Proof",
                    template="plotly_dark",
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)

            # Quantum Tunneling Spiral
            if any(x in p_low for x in ["tunnel", "quantum", "barrier"]):

                t = np.linspace(0, 10, 500)

                x = np.sin(t * 8)
                y = np.cos(t * 8)
                z = t

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter3d(
                        x=x,
                        y=y,
                        z=z,
                        mode='lines',
                        line=dict(width=6)
                    )
                )

                fig.update_layout(
                    title="Quantum Tunneling: 3D Spiral Migration",
                    template="plotly_dark",
                    height=700,
                    scene=dict(
                        xaxis_title="X",
                        yaxis_title="Y",
                        zaxis_title="Helical Depth"
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })

        except Exception as e:
            st.error(f"⚠️ Connection Jitter: {str(e)}")
