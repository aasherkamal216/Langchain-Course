import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Gemini Q/A Chatbot"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers the questions of the user."),
        ("user", "Questioin: {question}")
    ]
)

# Generating response
def get_response(question, api_key, model, temperature, max_tokens):
    llm = ChatGoogleGenerativeAI(model=model,
                                 temperature=temperature,
                                 google_api_key=api_key,
                                 max_output_tokens=max_tokens)
    
    parser = StrOutputParser()
    chain = prompt | llm | parser
    
    response = chain.invoke({"question": question})
    return response

## Streamlit code
st.title('Gemini :blue[Q/A Chatbot]')

with st.sidebar:
    st.header("Settings:")
    with st.popover("🔐 Google API Key", use_container_width=True):
        api_key = st.text_input("Insert your API Key here", type="password")

    model = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"])


    temperature = st.slider("Temperature",
                                min_value=0.0,
                                max_value=1.0,
                                step=0.2, value=0.5)
    
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, step=200, value=500)


if api_key:
    if question := st.text_input("Please enter your question."):
        response = get_response(question, api_key, model, temperature, max_tokens)
        st.write(response)
else:
    st.info("Please enter your API Key to proceed")