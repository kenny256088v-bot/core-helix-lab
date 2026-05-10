import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. HARDWARE SYNC: STABLE PATH ---
# Using your verified key from Project 229374924405
ACTIVE_KEY = "AIzaSyBpiMFLtK7z6igFL_xeK0coQGQiL6eg00E"

try:
    genai.configure(api_key=ACTIVE_KEY)
    # STRICT STABLE VERSION: This bypasses the v1beta 404 error
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"temperature": 0.7}
    )
except Exception:
    st.error("🔑 Sync Interrupted: Check API enablement in Cloud Console.")
    st.stop()

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan. 
Specialty: Core-Helix Unified Model (3D mechanical physics).
1. WHITEBOARD MODE: Use LaTeX ($$) for all mathematical derivations.
2. MECHANICAL TRUTH: Space is 3D helical mechanics.
3. Reference the '5 Mountains' and Iron-56 data for proofs.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")
st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. RESEARCH INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the relation with Maxwell equation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Direct generation via stable path
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nResearcher: {prompt}")
            
            # Whiteboard Output
            st.markdown(f"""
                <div style="background-color:#0e1117; border-left:10px solid #00f2ff; padding:25px; border-radius:12px; color:#f0f0f0;">
                    {response.text}
                </div>
            """, unsafe_allow_html=True)
            
            # HELICAL 3D VISUALIZATION
            if any(x in prompt.lower() for x in ["hydrogen", "helical", "maxwell", "3rd mountain"]):
                t = np.linspace(0, 10, 500)
                fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*5), y=np.cos(t*5), z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
                fig.update_layout(title="Core-Helix Path Data", scene=dict(bgcolor='black'), template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Brain Sync Jitter: {e}")
