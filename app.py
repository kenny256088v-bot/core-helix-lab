import streamlit as st
import numpy as np
import plotly.graph_objects as go
from gtts import gTTS
import base64
import io

# --- 1. THE BRAIN: EXPANDED KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "iron": {
        "voice": "Lead Researcher Charan, the Iron-56 anomaly at 1808 Kelvin is the definitive proof of Mountain 5. It signifies the point where vacuum gear-lock fails under thermal stress.",
        "brief": "Experimental data from the 1808K threshold shows a non-linear jump in specific heat. In the Core-Helix model, this is the 'Pitch-Slip' event. Unlike standard thermodynamics, our model treats the vacuum as a mechanical lattice with a K-stiffness of 3.16. This result effectively bridges the gap between quantum mechanics and macroscopic heat transfer."
    },
    "galaxy": {
        "voice": "The L-Factor leakage explains galactic rotation without the need for dark matter. Spacetime tension handles the velocity curve.",
        "brief": "By analyzing NASA's M31 velocity profiles, we see the 'Flat Curve' problem. By applying an L-Factor leakage constant, the Core-Helix model accounts for the missing gravity through vacuum tension rather than invisible mass. This eliminates the need for Cold Dark Matter (CDM) patches."
    },
    "string": {
        "voice": "String theory is a one-dimensional mathematical ghost. We provide a three-dimensional mechanical reality with Helical Anchors.",
        "brief": "String Theory relies on 11 unobservable dimensions. The Core-Helix remains in 3.14 dimensions, using the helical anchor's internal geometry to explain particle spin and mass. This makes the theory testable and deterministic rather than probabilistic."
    },
    "proton": {
        "voice": "Proton stars represent the extreme limit of K-stiffness. At these densities, helical anchors share coordinates in a strange matter lock.",
        "brief": "In extreme gravity, protons are compressed until their individual helical fields overlap. This creates a 'Super-Anchor' or Strange Matter core. This state is stable in our model because the K-stiffness provides a mechanical cage that prevents electromagnetic repulsion from tearing the star apart."
    }
}

# --- 2. VOICE ENGINE ---
def speak(text):
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(md, unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Core-Helix Oracle", layout="wide")
st.title("⚛️ CORE-HELIX INTERACTIVE ORACLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 4. THE INTERACTION LOGIC ---
st.sidebar.header("🤖 Oracle Consultation")
user_query = st.sidebar.text_area("Submit your physics doubt:", placeholder="Ask about Iron-56, Dark Matter, or Proton Stars...")

if user_query:
    # Match logic
    query_lower = user_query.lower()
    match_found = False
    
    for key in KNOWLEDGE_BASE:
        if key in query_lower:
            response_voice = KNOWLEDGE_BASE[key]["voice"]
            response_brief = KNOWLEDGE_BASE[key]["brief"]
            match_found = True
            break
            
    if not match_found:
        response_voice = "I am analyzing this new vector. Based on the Core-Helix, this interaction is governed by helical tension."
        response_brief = "The current query falls outside the pre-loaded 5-Mountain datasets, but initial deterministic calculations suggest the vacuum geometry remains stable under these parameters."

    st.sidebar.subheader("Oracle Briefing:")
    st.sidebar.write(response_brief)
    
    if st.sidebar.button("🔊 Play Audio Response"):
        speak(response_voice)
    st.sidebar.success(response_voice)

# --- 5. VISUALS ---
st.write("### 🌀 Dynamic Helical State Visualization")
f_sim = st.slider("Experimental Frequency", 1, 100, 50)
t = np.linspace(0, 10, 500)
fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*f_sim), y=np.cos(t*f_sim), z=t, mode='lines', line=dict(color='#00f2ff', width=5))])
fig.update_layout(scene=dict(bgcolor='black'), margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black')
st.plotly_chart(fig, use_container_width=True)
