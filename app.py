import streamlit as st
import numpy as np
import plotly.graph_objects as go
from gtts import gTTS
import base64
import io

# --- 1. THE STUDENT-FRIENDLY BRAIN ---
# This dictionary now uses "Core Concepts" to map many different questions to one simple explanation.
KNOWLEDGE_BASE = {
    "iron": {
        "voice": "Think of Iron-56 like a gear in a machine. At 1808 Kelvin, the gear finally slips. That's why the heat jumps!",
        "brief": "Imagine you're pedaling a bike. If the chain slips, you feel a jolt. In my theory, the 'Vacuum' is like that chain. At a specific heat, the chain slips (we call this a Pitch-Slip). Standard physics calls it an anomaly; we call it a mechanical limit of space itself!"
    },
    "galaxy": {
        "voice": "Galaxies don't need hidden dark matter. Space itself is just pulled tight like a giant rubber band!",
        "brief": "Why do the outer stars move so fast? Standard science says there's 'invisible' stuff pushing them. But I say space is like a trampoline. The further out you go, the more the 'L-Factor' or tension pulls back. It's like a rubber band holding the galaxy together—no mysterious 'dark' particles needed."
    },
    "string": {
        "voice": "String theory is like a flat drawing. Core-Helix is the real 3D object. It's much simpler to understand!",
        "brief": "String theory says everything is a tiny vibrating string in 11 hidden dimensions. That's hard to visualize, right? My theory says everything is a 3D Spiral (a Helix). It’s like the difference between a drawing of a spring and a real, bouncy metal spring you can actually touch."
    },
    "proton": {
        "voice": "A Proton Star is like a crowded elevator where everyone locks arms so they don't fall over. It's super stable!",
        "brief": "Usually, protons push each other away like the same ends of magnets. But in a Proton Star, the pressure is so high they 'Lock Gears.' They form one giant, solid structure. It sounds impossible, but it's just a 3D mechanical puzzle solved by high pressure!"
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

# --- 3. UI STYLE ---
st.set_page_config(page_title="Charan's Helix Lab", layout="wide")
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.2rem; color: #00f2ff; background-color: #101010; }
    .stMarkdown p { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX INTERACTIVE ORACLE")
st.subheader("Interactive Student Edition | Lead Researcher: Charan")

# --- 4. THE INTERACTIVE CHAT ---
st.sidebar.header("🤖 Ask me anything!")
user_query = st.sidebar.text_area("What's confusing you?", placeholder="Try: 'Why is Iron-56 weird?' or 'Is Dark Matter real?'")

if user_query:
    q = user_query.lower()
    # Smarter keyword detection
    if any(x in q for x in ["iron", "56", "jump", "heat"]):
        data = KNOWLEDGE_BASE["iron"]
    elif any(x in q for x in ["galaxy", "dark matter", "space", "stars"]):
        data = KNOWLEDGE_BASE["galaxy"]
    elif any(x in q for x in ["string", "dimension", "dimensions"]):
        data = KNOWLEDGE_BASE["string"]
    elif any(x in q for x in ["proton", "star", "strange", "impossible"]):
        data = KNOWLEDGE_BASE["proton"]
    else:
        data = {
            "voice": "That's a great question! I'm checking the 5 Mountains data for that now.",
            "brief": "I don't have a specific 'Simplified Brief' for that yet, but everything in this lab follows the same rule: Space is mechanical, not magical. Try asking about the Galaxies or the Proton Stars!"
        }

    st.sidebar.markdown(f"**The Simple Explanation:**\n\n{data['brief']}")
    
    if st.sidebar.button("🔊 Listen to Oracle"):
        speak(data['voice'])
    st.sidebar.success(data['voice'])

# --- 5. VISUALS ---
st.write("### 🌀 See the Helix in Action")
f_sim = st.slider("Energy Level", 1, 100, 45)
t = np.linspace(0, 10, 500)
fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*f_sim), y=np.cos(t*f_sim), z=t, mode='lines', line=dict(color='#00f2ff', width=8))])
fig.update_layout(scene=dict(bgcolor='black', xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)), margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black')
st.plotly_chart(fig, use_container_width=True)
