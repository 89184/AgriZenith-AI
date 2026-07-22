import streamlit as st
import textwrap

def render_header():
    header_html = textwrap.dedent("""
    <div style="background: linear-gradient(135deg,#0A2540 0%,#1E3A8A 50%,#3B82F6 100%);padding: 2rem;border-radius: 15px;margin-bottom: 2rem;color: white;text-align: center;box-shadow: 0 8px 20px rgba(0,0,0,0.15);"><h1 style="font-size: 3rem;font-weight: 700;margin: 0;letter-spacing: -0.5px;">AgriZenith AI</h1>
        <p style="font-size: 1.3rem;opacity: 0.95;margin-top: 0.2rem;">An Multi-Stage Intent Classification and Retrieval Framework for Intelligent Agricultural Advisory, with an Artificial Intelligence that brings agriculture to its highest level of intelligence, efficiency, and innovation.</p><p style="font-size: 0.9rem;opacity: 0.8;">Powered by RAG, LLMs, and Domain‑specific with localized Knowledge</p>
    </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)