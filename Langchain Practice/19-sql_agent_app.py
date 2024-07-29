import streamlit as st
from pathlib import Path
import sqlite3
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from sqlalchemy import create_engine

# Page setup
st.set_page_config(page_icon="⚡", page_title="SQL Agent")
st.title("Langchain SQL Agent")

# Sidebar configuration
db_choice = st.sidebar.radio("Select Database:", ["Local Student DB", "PostgreSQL"])
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Database configuration
if db_choice == "Local Student DB":
    db_file_path = (Path(__file__).parent / "student.db").absolute()
    creator = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)
    db = SQLDatabase(create_engine("sqlite:///", creator=creator))

else:
    db_params = {
        "host": st.sidebar.text_input("Host:", value="localhost"),
        "port": st.sidebar.text_input("Port:", value="5432"),
        "user": st.sidebar.text_input("User:", value="postgres"),
        "password": st.sidebar.text_input("Password:", value="4321", type="password"),
        "database": st.sidebar.text_input("Database:", "projectdb")
    }
    db_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    db = SQLDatabase.from_uri(db_url)

# Agent setup
if api_key:
    llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=api_key, streaming=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent_executor_kwargs={"handle_parsing_errors": True},
    )

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you with the database?"}]

    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])

    if user_question := st.chat_input("Ask about the database:"):
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.chat_message("user").write(user_question)

        with st.chat_message("assistant"):
            response = agent.run(user_question, callbacks=[StreamlitCallbackHandler(st.container())])
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("Please enter your Groq API Key to start.")

# Clear chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with the database?"}]