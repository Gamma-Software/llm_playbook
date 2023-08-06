import os
from dotenv import load_dotenv

import streamlit as st
import st_pages
from st_pages import Page, Section


# Firstly load all the environment variables
load_dotenv()

# Secondly set the page config and the pages
st.set_page_config(
    page_title="LLM Use Cases",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Setup the OpenAI API key (can be retrieved from the environment
# variables or via the sidebar text input)
with st.sidebar:
    if "openai_api_key" not in st.session_state:
        if "OPENAI_API_KEY" in os.environ:
            st.session_state["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        else:
            st.session_state["openai_api_key"] = st.text_input(
                "OpenAI API Key", key="chatbot_api_key", type="password")

# Check if the OpenAI API key is set before continuing
if "openai_api_key" not in st.session_state:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Optional -- adds the title and icon to the current page
st_pages.add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
st_pages.show_pages(
    [
        Page("entrypoint.py", "Home", "🏠"),
        Section("Chatbots", icon="💬"),
        Page("streamlit_apps/chatbots/chatgptlike.py", "ChatGPT like", "💬"),
        Page("streamlit_apps/chatbots/tool_augmented_chatbot.py", "Tool Agent", "🔎"),
    ]
)