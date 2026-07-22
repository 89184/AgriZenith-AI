import streamlit as st

def render_query_input() -> str | None:
    """
    Renders the query input area and handles submission logic.

    Returns:
        str | None: The submitted query if valid, else None.
    """
    # Header
    st.markdown(
        """
        <h3 style="text-align:center;color:#1E3A8A;margin-bottom:20px;">
             Ask AgriZenith AI
        </h3>
        """,
        unsafe_allow_html=True,
    )

    # Text input
    query = st.text_area(
        label="Enter your question below:",
        height=120,
        placeholder="e.g., How to control fungal infection in wheat?",
        key="query_input",
        help="Ask questions related to crops, pests, soil, irrigation, weather, and fertilizers.",
    )

    # Centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button(
            "Get AI Advice",
            use_container_width=True,
            type="primary",
        )

    # Handle submission
    if submitted:
        if query.strip():
            # Store the submitted query in session state for later use
            st.session_state.submitted_query = query
            return query
        else:
            st.warning(" Please enter an agricultural question.")
            return None

    # If no new submission, return None
    return None