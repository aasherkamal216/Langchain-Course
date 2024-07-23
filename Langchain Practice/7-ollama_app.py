import os
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers the questions of the user"),
    ("user", "Questioin: {question}"),
])

# Ollama Model (local)
llm = ChatOllama(model="gemma:2b")

# Chain
chain = prompt | llm | StrOutputParser()

# streamlit code
st.set_page_config(page_icon=":mag:")
st.title("Ollama Chat Model")
question = st.text_input("Ask me a question...")

if question:
    response = chain.invoke({"question": question})
    st.write(response)