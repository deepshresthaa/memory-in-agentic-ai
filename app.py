"""Streamlit UI for the Mem0 + LangChain interview prep assistant."""

import streamlit as st
from memory_agent import chat, get_all_memories

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.chat-header {
    text-align: center;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    background-color: #111827;
}

.chat-header h1 {
    margin-bottom: 0;
}

.memory-box {
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.title("🧑 Candidate")

    user_id = st.text_input(
        "User ID",
        value="alice"
    )

    st.markdown("---")

    st.subheader("Interview Settings")

    st.info(
        """
        **Model:** llama-3.1-8b-instant
        
        **Memory:** Mem0 + Qdrant
        
        **Embeddings:** Gemini
        """
    )

    st.markdown("---")

    if st.button(
        "🧠 View Memories",
        use_container_width=True
    ):
        st.session_state["show_memories"] = True

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.pop("messages", None)
        st.rerun()

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown("""
<div class="chat-header">
    <h1>🧠 AI Interview Coach</h1>
    <p>
        Personalized interview preparation powered by
        LangChain, Groq and Mem0
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP INFO BAR
# -------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Candidate", user_id)

with c2:
    st.metric(
        "Conversation Turns",
        len(st.session_state.get("messages", []))
    )

with c3:
    st.metric(
        "Memory Status",
        "Active"
    )

# -------------------------------------------------
# MEMORY PANEL
# -------------------------------------------------

if st.session_state.get("show_memories", False):

    with st.expander(
        "Stored Candidate Memories",
        expanded=True
    ):
        st.json(get_all_memories(user_id))

# -------------------------------------------------
# CHAT STATE
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------

if user_input := st.chat_input(
    "Answer the interview question or ask for coaching..."
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing response and retrieving memories..."
        ):
            reply = chat(
                user_id=user_id,
                user_message=user_input
            )

        st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )