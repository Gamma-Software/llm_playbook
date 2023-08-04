import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from streamlit_apps.chatbots.utils import reset_chatbot_messages, load_session_messages

st.title("🔎 LangChain - Chat with search")
openai_api_key = st.session_state["openai_api_key"]

key_message = "searchagent-messages"

reset_chatbot_messages(key_message, "I'm the 🔎 LangChain - Search Agent. "
                       "What do you want to search for ?")

load_session_messages(key_message)

if prompt := st.chat_input(placeholder="For instance: Who won the Women's U.S. Open in 2018?"):
    st.session_state[key_message].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)

    # Create the search tool (with DuckDuckGo)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                    handle_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state[key_message], callbacks=[st_cb])
        st.session_state[key_message].append({"role": "assistant", "content": response})
        st.write(response)
