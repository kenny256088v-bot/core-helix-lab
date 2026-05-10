import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN CONFIGURATION ---
# Using your provided API Key
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg") 
model = genai.GenerativeModel('gemini-1.5-flash-latest')

SYSTEM_PROMPT = """
You are Charan's Research Partner at IIIT Kurnool. You represent the 'Core-Helix Unified Model'.
1. When asked about standard physics (like Quantum Tunneling), explain how the 'Helix Pitch-Jump' is the real mechanical cause.
2. If asked for a derivation, always use LaTeX ($$) for math. Use deep-dive technical paragraphs.
3. Be bold. Explain why String Theory fails (1D) and why Core-Helix succeeds (3D mechanical).
4. Address the user as 'Lead Researcher' or 'Charan'.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM WHITEBOARD STYLE ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #0e1117;
        border-left: 5px solid #00f2ff;
        padding: 25px;
        border-radius: 5px;
        font-family: 'serif';
        color: #e0e0e0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-size: 1.2em;">PARTNER STATUS: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. AUTOMATIC GRAPH LOGIC ---
def plot_mountain_5():
    x = np.linspace(1700, 1900, 100)
    core_helix = np.where(x > 1808, 15, 0) 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=core_helix, name="Observed Pitch-Slip", line=dict(color='#00f2ff', width=4)))
    fig.update_layout(title="Mountain 5: Iron-56 Thermal Anomaly (1808K)", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

def plot_tunneling():
    t = np.linspace(0, 10, 500)
    # Visualizing a helix threading through a potential barrier
    x = np.sin(t*12)
    y = np.cos(t*12)
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=t, mode='lines', line=dict(color='#7000ff', width=6))])
    fig.update_layout(title="Quantum Tunneling: Helical Threading Visualization", scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE CHAT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Partner, explain the derivation for Mountain 1..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini Brain Power
    full_query = f"{SYSTEM_PROMPT}\n\nResearcher Question: {prompt}"
    response = model.generate_content(full_query)
    
    with st.chat_message("assistant"):
        # Wrap the response in our custom "Whiteboard" style
        st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
        
        # Trigger graphs automatically based on the conversation topic
        p_low = prompt.lower()
        if any(word in p_low for word in ["tunnel", "barrier", "quantum"]):
            plot_tunneling()
        if any(word in p_low for word in ["iron", "56", "heat", "thermal", "mountain 5"]):
            plot_mountain_5()

    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
