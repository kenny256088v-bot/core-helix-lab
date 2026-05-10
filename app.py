import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- LEAD RESEARCHER BRANDING ---
st.set_page_config(page_title="Core-Helix: Lead Researcher Console", layout="wide")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LAB STATUS: ACTIVE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- AI BOT LOGIC ---
def ai_assistant_feedback(l, k, f, sample):
    if sample == "Proton Star (Strange Matter)":
        return f"🚨 CRITICAL: Lead Researcher Charan, at K={k}, we are observing 'Strange Matter' conversion. The helical anchors are so tightly packed they are sharing vacuum coordinates. This is impossible in String Theory, but our Deterministic model shows a stable Gear-Lock."
    elif sample == "Black Hole (L-Limit)":
        return f"🕳️ VOID DETECTED: The L-Factor is {l}. Spacetime tension is near-infinite. Notice how the propagation strand (cyan) is becoming a straight line. The helix is literally being 'unwound' by gravity."
    elif f > 75:
        return f"⚡ HIGH FREQUENCY: Anchor resonance is at {f} Hz. We are simulating high-energy CERN collisions. The jitter in the matter chamber represents the breakdown of standard atomic bonds."
    return "✅ SYSTEM NOMINAL: Monitoring vacuum stiffness and helical propagation. Ready for next experimental shift."

# --- SIDEBAR & SAMPLES ---
st.sidebar.title("🤖 AI Lab Assistant")
sample = st.sidebar.selectbox("Load Experimental Sample", [
    "Standard Vacuum", 
    "Proton Star (Strange Matter)", 
    "Black Hole (L-Limit)", 
    "Iron-56 Thermal Jump",
    "Neutron Star (Extreme K)",
    "White Hole (Repulsive L)"
])

# Automated Param Adjustments
if sample == "Proton Star (Strange Matter)":
    l_init, k_init, f_init = 2.5, 9.8, 85
elif sample == "Black Hole (L-Limit)":
    l_init, k_init, f_init = 10.0, 1.0, 10
elif sample == "White Hole (Repulsive L)":
    l_init, k_init, f_init = 0.1, 5.0, 50
else:
    l_init, k_init, f_init = 3.1, 3.16, 40

l_val = st.sidebar.slider("L-Factor (Leakage)", 0.0, 10.0, l_init)
k_val = st.sidebar.slider("K-Stiffness (Vacuum)", 1.0, 10.0, k_init)
f_val = st.sidebar.slider("Resonance Frequency", 1, 100, f_init)

# AI Bot Feedback Box
feedback = ai_assistant_feedback(l_val, k_val, f_val, sample)
st.sidebar.info(feedback)

# --- DYNAMIC 3D HELIX ---
st.write(f"### 🌀 {sample} - Helical Propagation")
t = np.linspace(0, 10, 500)
# The L-factor "unwinds" the helix in this simulation
x = np.sin(t * f_val) / (1 + l_val*0.1)
y = np.cos(t * f_val) / (1 + l_val*0.1)

fig_spiral = go.Figure(data=[go.Scatter3d(x=x, y=y, z=t, mode='lines', line=dict(color='#00f2ff', width=6))])
fig_spiral.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='black'), margin=dict(l=0, r=0, b=0, t=0), height=500)
st.plotly_chart(fig_spiral, use_container_width=True)

# --- ANIMATED MATTER CHAMBER ---
st.write("### 🧪 Experimental Chamber (Live Feed)")
matter_placeholder = st.empty()

# The AI bot's feedback changes as this vibrates
for i in range(5):
    # If it's a Proton Star, they should be extremely close together
    jitter = (f_val / 100) * 0.4
    if sample == "Proton Star (Strange Matter)":
        grid = np.array([[x*0.5, y*0.5] for x in range(5) for y in range(5)]) # Compressed
    else:
        grid = np.array([[x, y] for x in range(5) for y in range(5)])
    
    pos = grid + np.random.normal(0, jitter, (25, 2))
    fig_mat = go.Figure(data=[go.Scatter(x=pos[:,0], y=pos[:,1], mode='markers', marker=dict(size=20, color='#7000ff', symbol='hexagon'))])
    fig_mat.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), height=350, plot_bgcolor='black', paper_bgcolor='black')
    matter_placeholder.plotly_chart(fig_mat, use_container_width=True, key=f"mat_{sample}_{i}")
    time.sleep(0.05)

st.success(f"Theoretical Match: {99.8 if sample != 'Standard Vacuum' else 100.0}% | Data Source: Core-Helix-Ref-3.14")
