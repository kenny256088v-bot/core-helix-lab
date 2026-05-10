import os
import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# =========================================
# GEMINI SETUP
# =========================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Missing Gemini API Key")
    st.stop()

genai.configure(api_key=API_KEY)

# Updated stable model
model = genai.GenerativeModel("gemini-2.0-flash")

# =========================================
# SYSTEM PROMPT
# =========================================

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan.

Specialty:
Core-Helix Unified Model (3D mechanical physics)

Rules:
1. Use LaTeX for derivations.
2. Explain physics through 3D helical mechanics.
3. Maintain professional technical tone.
"""

# =========================================
# STREAMLIT CONFIG
# =========================================

st.set_page_config(
    page_title="Core-Helix Research Console",
    layout="wide"
)

# =========================================
# STYLING
# =========================================

st.markdown("""
<style>
.whiteboard {
    background-color: #0e1117;
    border-left: 8px solid #00f2ff;
    padding: 25px;
    border-radius: 12px;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")

st.markdown(
    "<p style='color:#00f2ff;font-weight:bold;'>PARTNER STATUS: ACTIVE</p>",
    unsafe_allow_html=True
)

# =========================================
# CHAT MEMORY
# =========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# DISPLAY CHAT
# =========================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================
# INPUT
# =========================================

prompt = st.chat_input(
    "Partner, explain the derivation for..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            full_prompt = f"""
{SYSTEM_PROMPT}

Researcher:
{prompt}
"""

            response = model.generate_content(full_prompt)

            answer = response.text

            st.markdown(
                f'<div class="whiteboard">{answer}</div>',
                unsafe_allow_html=True
            )

            # =========================================
            # HELICAL VISUALIZATION
            # =========================================

            if any(
                x in prompt.lower()
                for x in ["hydrogen", "helical", "rotation"]
            ):

                t = np.linspace(0, 10, 500)

                x = np.sin(t * 5)
                y = np.cos(t * 5)
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
                    title="Helical Path Projection",
                    template="plotly_dark",
                    height=700
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error(f"⚠️ Brain Sync Jitter: {str(e)}")
