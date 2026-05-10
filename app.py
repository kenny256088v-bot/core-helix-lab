import streamlit as st
import numpy as np
import plotly.graph_objects as go
from gtts import gTTS
import base64
import io

# --- BRANDING & VOICE ENGINE ---
st.set_page_config(page_title="Core-Helix Oracle", layout="wide")

def speak(text):
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(md, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX INTERACTIVE ORACLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LEAD RESEARCHER: CHARAN | MODEL: DETERMINISTIC V3.14</p>', unsafe_allow_html=True)

# --- THE "IMPOSSIBLE" KNOWLEDGE BASE ---
EXPERIMENTAL_DATA = {
    "Proton Star": "A theoretical stellar remnant where K-Stiffness exceeds 9.5. Unlike standard stars, protons are forced into a singular helical 'strange matter' lock, defying standard EM repulsion.",
    "Black Hole L-Limit": "The point where L-Factor leakage reaches 10.0. The helical strand unwinds completely, creating the illusion of a singularity.",
    "Iron-56 Jump": "The 1808K phase shift is the mechanical evidence of vacuum gear-lock slippage. It is the most realistic proof of Mountain 5."
}

# --- AI CHAT INTERFACE ---
st.sidebar.header("🤖 Oracle Consultation")
user_input = st.sidebar.text_area("Challenge the Theory:", placeholder="Ask about the 5 Mountains or specific anomalies...")

if user_input:
    # Logic for detailed brief
    if "proton" in user_input.lower():
        brief = EXPERIMENTAL_DATA["Proton Star"]
        response = "Lead Researcher Charan, a Proton Star is the ultimate proof of our model. While String Theory requires extra dimensions to explain stability, our K-Stiffness provides a 3D mechanical cage."
    elif "iron" in user_input.lower():
        brief = EXPERIMENTAL_DATA["Iron-56 Jump"]
        response = "Observing Mountain 5. The thermal jump at 1808 Kelvin is not noise—it is the deterministic lattice reaching its stress limit."
    else:
        brief = "Analyzing new experimental vector..."
        response = "System analyzing. Based on the Core-Helix, this interaction remains governed by deterministic helical tension."

    st.sidebar.markdown(f"**Brief:** {brief}")
    if st.sidebar.button("🔊 Hear Oracle Response"):
        speak(response)
    st.sidebar.success(response)

# --- 3D VISUALIZATION ---
sample = st.selectbox("Current Simulation Target", ["Standard Vacuum", "Proton Star", "Black Hole Horizon"])
freq = st.slider("Resonance Frequency", 1, 100, 85 if sample == "Proton Star" else 50)

t = np.linspace(0, 10, 500)
# Visualizing the "impossible" geometry
x = np.sin(t * freq) * (0.5 if sample == "Proton Star" else 1.0)
y = np.cos(t * freq) * (0.5 if sample == "Proton Star" else 1.0)

fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=t, mode='lines', line=dict(color='#00f2ff', width=7))])
fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='black'),
                  margin=dict(l=0, r=0, b=0, t=0), height=600, paper_bgcolor='black')
st.plotly_chart(fig, use_container_width=True)

st.info("Status: AI Oracle Online. Voice feedback enabled for Lead Researcher authentication.")
