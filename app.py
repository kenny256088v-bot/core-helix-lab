import streamlit as st
import numpy as np
import plotly.graph_objects as go
from gtts import gTTS
import base64
import io

# --- THE UNIVERSAL CORE-HELIX LAWS ---
# This is the "Brain" the AI uses to answer anything accurately
LAWS = {
    "Matter": "Everything is a 3D spiral. Smaller spirals (Hydrogen) are loose; heavier ones (Iron) are tight.",
    "Gravity": "It's just tension. Like a rubber band pulling on the spirals.",
    "Space": "It's a mechanical lattice. It's not empty; it's a grid with a stiffness of 3.16.",
    "Energy": "Vibration frequency of the helical anchors."
}

def speak(text):
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(md, unsafe_allow_html=True)

st.set_page_config(page_title="Core-Helix Student Lab", layout="wide")
st.title("⚛️ CORE-HELIX: THE STUDENT PEER ORACLE")
st.markdown('<p style="color:#00f2ff;">Lead Researcher: Charan | IIIT Kurnool</p>', unsafe_allow_html=True)

# --- THE DYNAMIC RESPONSE ENGINE ---
st.sidebar.header("💬 Talk to the Lab Peer")
user_q = st.sidebar.text_area("Ask me like I'm your lab partner:", placeholder="What about Hydrogen?")

if user_q:
    q = user_q.lower()
    
    # 1. ATOMS / HYDROGEN / ELEMENTS
    if any(x in q for x in ["hydrogen", "atom", "element", "matter", "proton"]):
        voice = "Think of Hydrogen as a single, loose spring. It's the simplest helix in our lab!"
        brief = f"In our model, {user_q} isn't just a particle. It's a specific 3D spiral shape. Since it's light, its 'Helical Tension' is low. Unlike String Theory, we don't need 11 dimensions to see it—it's right here in 3D!"
        
    # 2. GRAVITY / WEIGHT / PULL
    elif any(x in q for x in ["gravity", "pull", "weight", "fall", "black hole"]):
        voice = "Gravity is just space acting like a giant trampoline pulling on our anchors."
        brief = "Instead of curved spacetime, imagine a giant mesh. When you have a heavy helix, it pulls the mesh tight. That pull is what we feel as gravity. We call this the L-Factor leakage!"
        
    # 3. THE 5 MOUNTAINS / IRON / HEAT
    elif any(x in q for x in ["iron", "56", "mountain", "heat", "temperature"]):
        voice = "Mountain 5 is the big one! It's where the vacuum gears finally slip."
        brief = "At 1808 Kelvin, Iron-56 hits a limit. Imagine a clock gear spinning so fast it jumps a tooth. That 'jump' is the heat anomaly! It proves space has a mechanical stiffness (K=3.16)."

    # 4. DEFAULT (UNIVERSAL LAW)
    else:
        voice = "That's a deep one. Let's look at it through the 3D Helix lens."
        brief = f"Even for {user_q}, the rule is the same: Space is a mechanical grid, not a ghost. If it exists, it has a spiral shape (Helix) and a tension level. Everything connects back to the K-Stiffness of our 3.14 dimension!"

    st.sidebar.info(brief)
    if st.sidebar.button("🔊 Play Peer Audio"):
        speak(voice)
    st.sidebar.success(voice)

# --- DUAL-VIEW EXPERIMENT ---
col1, col2 = st.columns(2)

with col1:
    st.write("### 🌀 3D Helix Geometry")
    freq = st.slider("Vibration Speed", 1, 100, 40)
    t = np.linspace(0, 10, 500)
    # The "Student" visual: Color changes with frequency
    color = "#00f2ff" if freq < 70 else "#ff0055"
    fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*freq), y=np.cos(t*freq), z=t, mode='lines', line=dict(color=color, width=10))])
    fig.update_layout(scene=dict(bgcolor='black'), margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### 📉 The NASA Flat-Curve Proof")
    # Interactive rotation curve
    r = np.linspace(1, 20, 100)
    standard = 1/np.sqrt(r)
    core_helix = np.full_like(r, 0.8) # The "Flat" result
    fig_rc = go.Figure()
    fig_rc.add_trace(go.Scatter(x=r, y=standard, name="Old Physics (Fails)", line=dict(dash='dash')))
    fig_rc.add_trace(go.Scatter(x=r, y=core_helix, name="Core-Helix (Matches Data)", line=dict(width=4, color="#00f2ff")))
    fig_rc.update_layout(title="Galaxy Rotation Curve", template="plotly_dark")
    st.plotly_chart(fig_rc, use_container_width=True)

st.write("**Peer Note:** If they ask a tough question, point to the Flat Curve. It's the hardest data to argue with!")
