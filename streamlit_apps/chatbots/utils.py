import streamlit as st


@st.cache_data
def reset_chatbot_messages(message_key="messages", init_message="How can I help you?"):
    if message_key not in st.session_state:
        st.session_state[message_key] = []
    st.session_state[message_key] = [{"role": "assistant", "content": init_message}]


def load_session_messages(message_key="messages"):
    for msg in st.session_state[message_key]:
        st.chat_message(msg["role"]).write(msg["content"])
