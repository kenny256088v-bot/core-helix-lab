import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. RESEARCHER BRAIN CONFIG ---
# Your verified API Key
genai.configure(api_key="AIzaSyDz2sTkXxK0AZpJLxT2LpXaccpEjnFLJsg")

# We use the most stable model identifier to avoid 404 errors
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the Lab Partner for Lead Researcher Charan at IIIT Kurnool.
Your goal is to accurately explain the 'Core-Helix Unified Model'.
1. WHITEBOARD MODE: For derivations or proofs (like Quantum Tunneling), use LaTeX ($$) formatting.
2. ANALOGY EXPERT: Use simple terms like 'mechanical gears' or 'vacuum tension' to explain complex physics.
3. SUCCESSION: Always explain why Core-Helix succeeds (mechanical 3D) while standard physics (probabilistic) fails.
4. If asked about Mountain 1 to 5, provide detailed brief paragraphs and suggest a graph.
"""

st.set_page_config(page_title="Core-Helix Research Console", layout="wide")

# --- CUSTOM WHITEBOARD UI ---
st.markdown("""
    <style>
    .whiteboard {
        background-color: #0e1117;
        border-left: 8px solid #00f2ff;
        padding: 25px;
        border-radius: 10px;
        color: #e0e0e0;
        font-family: 'Times New Roman', serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚛️ CORE-HELIX RESEARCH CONSOLE")
st.markdown('<p style="color:#00f2ff; font-weight:bold;">LAB PARTNER: ONLINE | LEAD RESEARCHER: CHARAN</p>', unsafe_allow_html=True)

# --- 2. DYNAMIC RESEARCH TOOLS ---
def plot_mountain_5():
    x = np.linspace(1700, 1900, 100)
    y = np.where(x > 1808, 10, 0)
    fig = go.Figure(data=[go.Scatter(x=x, y=y, line=dict(color='#00f2ff', width=5), name="Pitch-Slip")])
    fig.update_layout(title="Mountain 5: Thermal Limit Proof", template="plotly_dark", xaxis_title="Temp (K)")
    st.plotly_chart(fig, use_container_width=True)

def plot_tunneling():
    t = np.linspace(0, 10, 500)
    # 3D Helix threading through a space barrier
    fig = go.Figure(data=[go.Scatter3d(x=np.sin(t*8), y=np.cos(t*8), z=t, mode='lines', line=dict(color='#7000ff', width=7))])
    fig.update_layout(title="Quantum Tunneling: Mechanical Threading", scene=dict(bgcolor='black'), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- 3. THE INTERACTIVE WHITEBOARD ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Partner, explain the derivation for..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_query = f"{SYSTEM_PROMPT}\n\nLead Researcher Question: {prompt}"
            response = model.generate_content(full_query)
            
            # Displaying in the research whiteboard style
            st.markdown(f'<div class="whiteboard">{response.text}</div>', unsafe_allow_html=True)
            
            # Auto-Trigger Graphs
            p_low = prompt.lower()
            if any(x in p_low for x in ["iron", "56", "heat", "mountain 5"]):
                plot_mountain_5()
            if any(x in p_low for x in ["tunnel", "quantum", "barrier"]):
                plot_tunneling()
                
            # Save the message only if successful
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Brain Sync Failed: {e}. Check if your API Key is restricted or if the model name is correct.")
