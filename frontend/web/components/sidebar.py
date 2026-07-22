import streamlit as st

def render_sidebar():
    with st.sidebar:
        
        st.markdown("""<h2 style="text-align:center;color:#1E3A8A;margin-bottom:10px;">Query History</h2>""",unsafe_allow_html=True)

        if "history" in st.session_state and st.session_state.history:
            for idx, item in enumerate(reversed(st.session_state.history)):
                q = item["query"]
                short_q = q[:50] + "..." if len(q) > 50 else q
                if st.button(f"🔹 {short_q}", key=f"hist_{idx},use_container_width=True"):
                    st.session_state.current_result = item["result"]
                    st.session_state.current_query = item["query"]
                    st.rerun()
        else:
            st.caption("No agricultural queries have been submitted yet.")

        st.markdown("---")

        st.markdown("""
            ### AgriZenith AI

            - Multi-Stage Intent Classification
            - Retrieval-Augmented Generation (RAG)
            - Domain-Specific Knowledge
            - Intelligent Agricultural Advisory
            """
        )