import os
        # AUTO WHITEBOARD
        # ==================================

        if whiteboard_mode:

            if detected["quantum"]:
                self.whiteboard.quantum_derivation()

            if detected["gravity"]:
                self.whiteboard.gravity_derivation()

        # ==================================
        # AUTO VISUALIZATION
        # ==================================

        if visualization_mode:

            if detected["quantum"]:
                self.visual.quantum_tunneling()

            if detected["helical"]:
                self.visual.helical_projection()

            if detected["gravity"]:
                self.visual.gravity_field()

            if detected["nuclear"]:
                self.visual.nuclear_binding()

        st.session_state.research_memory.append(prompt)

        return answer

# ==========================================
# MAIN CHAT LOOP
# ==========================================

orchestrator = ResearchOrchestrator()

prompt = st.chat_input(
    "Lead Researcher, enter your physics investigation..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            answer = orchestrator.run(prompt)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error(f"⚠️ Research Engine Error: {str(e)}")
