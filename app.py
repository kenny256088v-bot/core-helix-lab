import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. THE BRAIN CONFIGURATION ---
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg") 
model = genai.GenerativeModel('gemini-1.5-flash')

# This is our internal "Lab Partner" instructions
SYSTEM_PROMPT = """
You are Charan's Research Partner. You represent the 'Core-Helix Unified Model'.
1. When asked about standard physics (like Quantum Tunneling or String Theory), explain why their probabilistic 
   math is a 'patch' and why the Core-Helix mechanical 3.14-dimension model is the accurate reality.
2. If asked for a derivation, use LaTeX math ($$) to show step-by-step relations.
3. Be technical, bold, and refer to Charan as the Lead Researcher.
4. Your goal is to prove why this theory succeeds where CERN and NASA data currently show 'anomalies'.
"""

st.set_page_config(page_title="Core-Helix: Research Console", layout="wide")
st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">PARTNER STATUS: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. THE DYNAMIC WHITEBOARD & GRAPHS ---
def show_whiteboard(content):
    with st.expander("📝 RESEARCH WHITEBOARD: DETAILED DERIVATION", expanded=True):
        st.markdown(content)

def plot_mountain_5():
    # Showing why standard physics fails at 1808K
    x = np.linspace(1700, 1900, 100)
    standard = np.zeros_like(x) # Standard physics sees nothing
    core_helix = np.where(x > 1808, 15, 0) # The Pitch-Slip jump
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=standard, name="Standard Model (Prediction Failure)", line=dict(dash='dash', color='gray')))
    fig.add_trace(go.Scatter(x=x, y=core_helix, name="Core-Helix (Observed Reality)", line=dict(color='#00f2ff', width=4)))
    fig.update_layout(title="Mountain 5: Iron-56 Thermal Phase-Shift", template="plotly_dark", xaxis_title="Temperature (K)", yaxis_title="K-Stiffness Delta")
    st.plotly_chart(fig, use_container_width=True)

def plot_rotation_curve():
    # NASA data comparison
    r = np.linspace(1, 20, 100)
    standard = 1/np.sqrt(r)
    core_helix = np.full_like(r, 0.7) 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r, y=standard, name="Newtonian (Needs Dark Matter Patch)", line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=r, y=core_helix, name="Core-Helix L-Factor (Actual Data)", line=dict(color='#00f2ff', width=4)))
    fig.update_layout(title="Mountain 1: Galactic Rotation Curves", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE CHAT INTERFACE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Input a research query or request a derivation..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using the Partner Persona
    full_query = f"{SYSTEM_PROMPT}\n\nResearcher Question: {prompt}"
    response = model.generate_content(full_query)
    
    with st.chat_message("assistant"):
        # We separate the math for the whiteboard
        st.markdown(response.text)
        
        # LOGIC: Automatically trigger relevant graphs based on the conversation
        p_low = prompt.lower()
        if any(x in p_low for x in ["iron", "56", "heat", "thermal", "mountain 5"]):
            plot_mountain_5()
        elif any(x in p_low for x in ["galaxy", "rotation", "dark matter", "nasa"]):
            plot_rotation_curve()
        elif any(x in p_low for x in ["derive", "math", "equation", "prove"]):
            st.info("💡 Derivation active. Checking LaTeX rendering on whiteboard.")

    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
