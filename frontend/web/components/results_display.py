import streamlit as st

def render_results(result):
    st.markdown("---")
    
    intent = result.get("intent", "Unknown")
    conf = result.get("intent_confidence", 0.0)
    # Indian flag inspired: Green (high), Saffron (medium), Red (low)
    color = "#10B981" if conf > 0.7 else "#F59E0B" if conf > 0.4 else "#d32f2f"
    
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 6px solid {color};">
        <div style="display: flex; align-items: center; gap: 3rem;">
            <div style="margin-left: auto; background: #e3f2fd; padding: 0.3rem 1rem; border-radius: 20px; font-size: 1.6rem; color: #0d47a1;">INTENT: {conf:.2f}
            </div>            
            <div style="margin-left: auto; background: #e3f2fd; padding: 0.3rem 1rem; border-radius: 20px; font-size: 1.6rem; color: #0d47a1;">
            CONFIDENCE: {intent}
            </div>
            <div style="margin-left: auto; background: #e3f2fd; padding: 0.3rem 1rem; border-radius: 20px; font-size: 1.6rem; color: #0d47a1;">
                Retrieval: {result.get('retrieval_confidence', 0.0):.2f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- FIXED ANSWER SECTION ----
    entities = result.get("entities", [])
    badge = ""
    if entities:
        top = entities[0]
        badge = f'<span style="background: #e3f2fd; color: #0d47a1; padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.85rem; font-weight: 500; margin-left: 0.5rem;">{top["entity"]}: {top["value"]}</span>'

    answer = result.get("answer", "No answer generated.")
    st.markdown(f"""
    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #138808; margin: 1.5rem 0; font-size: 1.05rem; line-height: 1.7; color: #1a1a1a; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;">
            <span style="font-size: 1.2rem; font-weight: 600; color: #1a1a1a;">Answer</span>
            {badge}
        </div>
        <div style="margin-top: 0.5rem;">
            {answer}
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ---- END FIXED ANSWER ----

    context = result.get("context", "")
    if context and context.strip():
        with st.expander("View Retrieved Context"):
            st.text_area("", context, height=150, label_visibility="collapsed")
    else:
        st.info("No relevant context was retrieved from the knowledge base.")

    st.markdown("---")