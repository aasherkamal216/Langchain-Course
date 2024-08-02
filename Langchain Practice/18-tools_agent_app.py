import os, dotenv
dotenv.load_dotenv()
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Wikipedia Tool
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
# Arxiv Tool
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
# DuckDuckGo Search Tool
search = DuckDuckGoSearchRun(name="Internet Search")

# Streamlit Code
st.set_page_config(page_icon=":mag:", page_title="Tools & Agent")
st.title(":green[Langchain] Search Agent")

with st.sidebar:
    with st.popover("Add Groq API Key", use_container_width=True):
        api_key = st.text_input("Get Your Groq API Key [Here](https://console.groq.com/keys)", type="password")
    st.divider()
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>About the App✨</h1>", unsafe_allow_html=True)
    st.write("""Hi there! This is a langchain search agent app. First, you have to
             introduce your Groq API key. Then type your question and hit Enter, 
             the assistant will step by step retrieve the information relevant to
             your question from Wikipedia, Arxiv and DuckDuckGo Search and then it'll
             answer your question based on that information.""")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ]

for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

if api_key:
    if prompt := st.chat_input("What is Generative AI?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=api_key, streaming=True)
        tools = [wiki_tool, arxiv_tool, search]

        search_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, agent_executor_kwargs={"handle_parsing_errors": True})
        try:
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
                response = search_agent.run(st.session_state.messages, callbacks=[st_callback])
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Groq API key in the sidebar to proceed.")