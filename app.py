import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN CONFIGURATION ---
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg") 
# FIXED: Added 'models/' prefix to resolve NotFound error
model = genai.GenerativeModel('models/gemini-1.5-flash')

SYSTEM_PROMPT = """
You are Charan's Research Partner at IIIT Kurnool. You represent the 'Core-Helix Unified Model'.
1. When asked about standard physics (like Quantum Tunneling), explain how the 'Helix Pitch-Jump' is the real mechanical cause.
2. If asked for a derivation, always use LaTeX ($$) for math.
3. Be technical, accurate, and explain concepts simply using the 5 Mountains data.
4. If a graph is needed, mention 'Generating Graph' in your text.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM WHITEBOARD STYLE ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #1a1a1a;
        border: 2px solid #00f2ff;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. AUTOMATIC GRAPH LOGIC ---
def plot_mountain_5():
    x = np.linspace(1700, 1900, 100)
    core_helix = np.where(x > 1808, 15, 0) 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=core_helix, name="Mountain 5 Proof", line=dict(color='#00f2ff', width=4)))
    fig.update_layout(title="Iron-56 Thermal Phase-Shift (1808K)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def plot_tunneling_visual():
    t = np.linspace(0, 10, 500)
    # Visualizing a helix passing through a barrier
    x = np.sin(t*10)
    y = np.cos(t*10)
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=t, mode='lines', line=dict(color='#7000ff', width=6))])
    fig.update_layout(title="Quantum Tunneling: Helical Threading", scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE CHAT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Brain Processing
    full_query = f"{SYSTEM_PROMPT}\n\nResearcher Question: {prompt}"
    response = model.generate_content(full_query)
    
    with st.chat_message("assistant"):
        # Wrap the response in our custom "Whiteboard" style
        st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
        
        # Trigger graphs automatically
        p_low = prompt.lower()
        if "tunnel" in p_low:
            plot_tunneling_visual()
        if "iron" in p_low or "56" in p_low:
            plot_mountain_5()

    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
