import os, dotenv
dotenv.load_dotenv()
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

# Wikipedia Tool
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
# Arxiv Tool
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
# DuckDuckGo Search Tool
search = DuckDuckGoSearchRun(name="Internet Search")

# Streamlit Code
st.set_page_config(page_icon=":mag:", page_title="Tools & Agent")
st.title(":red[Langchain] Tools and Agent")

with st.sidebar:
    api_key = st.text_input("Enter Your Groq API Key:", type="password")

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

        search_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True)
        
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response = search_agent.run(st.session_state.messages, callbacks=[st_callback])
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please enter your API Key to proceed")