# First
import openai
import streamlit as st
from streamlit_apps.chatbots.utils import reset_chatbot_messages, load_session_messages

key_message = "chatgptlike-messages"

reset_chatbot_messages(key_message, "I'm the ChatbotGPT like. How can I help you?")

st.title("💬 ChatGPT Like")

load_session_messages(key_message)

if prompt := st.chat_input():
    if not st.session_state["openai_api_key"]:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state[key_message].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state[key_message])
    msg = response.choices[0].message
    st.session_state[key_message].append(msg)
    st.chat_message("assistant").write(msg.content)
