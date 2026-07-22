import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.web.components.header import render_header
from frontend.web.components.query_input import render_query_input
from frontend.web.components.results_display import render_results
from frontend.web.components.sidebar import render_sidebar
from frontend.web.utils.css import load_css

st.set_page_config(
    page_title="AgriBoot – Farmer Advisory",
    page_icon="🇮",
    layout="wide",
)

load_css()

def main():
    render_sidebar()
    render_header()
    query = render_query_input()

    if query:
        from backend.pipeline import farmer_advisory
        with st.spinner("Analyzing your question..."):
            try:
                result = farmer_advisory(query)
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({
                    "query": query,
                    "result": result,
                })
                st.session_state.current_result = result
                st.session_state.current_query = query
                render_results(result)
            except Exception as e:
                st.error(f" Error: {e}")
    else:
        if "current_result" in st.session_state:
            render_results(st.session_state.current_result)

    # Footer – Copyright notice (Indian context)
    st.markdown("""
    <div style="
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 2px solid #e0e0e0;
        text-align: center;
        color: #666;
        font-size: 0.85rem;
    ">
        © 2025 AgriBoot &bull; Made with  for Indian Farmers &bull; All rights reserved.
        <br>
        <span style="font-size: 0.75rem; color: #999;">
            This system is for informational purposes only. Always consult local agricultural experts.
        </span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()