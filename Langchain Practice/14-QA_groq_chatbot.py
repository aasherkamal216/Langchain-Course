import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Groq Q/A Chatbot"

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hi there! How can I help you today?")]

# Prompt Template
system_template = (
    """Given a chat history and the latest user question 
    which might reference context in the chat history, 
    Answer the user question in a polite and professional manner."""
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "Questioin: {question}")
    ]
)

# Generating response
def get_response(question, api_key, model, temperature, max_tokens):
    llm = ChatGroq(model=model,
                   temperature=temperature,
                   api_key=api_key,
                   max_tokens=max_tokens)
    
    parser = StrOutputParser()
    chain = prompt | llm | parser
    
    response = chain.invoke({"question": question, "chat_history": st.session_state.chat_history})
    return response

## Streamlit code
st.title('Groq :blue[Q/A Chatbot]')

with st.sidebar:
    st.header("Settings:")
    with st.popover("🔐 Groq API Key", use_container_width=True):
        api_key = st.text_input("Insert your API Key here", type="password")

    model = st.selectbox("Model", ["llama-3.1-8b-instant",
                                   "mixtral-8x7b-32768", "llama3-8b-8192",
                                   "gemma2-9b-it", "llama-3.1-70b-versatile"])


    temperature = st.slider("Temperature",
                                min_value=0.0,
                                max_value=1.0,
                                step=0.2, value=0.5)
    
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, step=200, value=500)


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


if api_key:
    if question := st.chat_input("Please enter your question."):
        st.session_state.chat_history.append(HumanMessage(content=question))

        with st.chat_message("Human"):
            st.write(question)

        with st.spinner("Thinking..."):
            response = get_response(question, api_key, model, temperature, max_tokens)

            with st.chat_message("AI"):
                st.write(response)
        st.session_state.chat_history.append(AIMessage(content=response))

else:
    st.info("Please enter your API Key to proceed")