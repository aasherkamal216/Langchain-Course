import os, dotenv
dotenv.load_dotenv()
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Gemini RAG Chatbot"
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(documents)
    return doc_chunks 

def get_vectorstore(doc_chunks):
    vectorstore = FAISS.from_documents(doc_chunks, CohereEmbeddings())
    return vectorstore

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

def get_rag_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()

    condense_q_system_template = (
    """Given a chat history and the latest user question 
    which might reference context in the chat history, 
    formulate a standalone question which can be understood 
    without the chat history. Do NOT answer the question, 
    just reformulate it if needed and otherwise return it as is."""
)
    condense_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", condense_q_system_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, condense_q_prompt)

    system_prompt = (
    """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer
    the question. If you don't know the answer, say that you
    don't know. Keep the answer concise.\n\n
    {context}
    """
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)
    return rag_chain

def get_conversational_rag_chain(rag_chain, question, session_id):
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain.invoke({"input": question},
                                           config={"configurable": {"session_id": session_id}})['answer']
 
# Streamlit code
st.title("Ultimate Gemini :red[RAG Chatbot]")
if 'vectorstore' not in st.session_state:
    st.session_state['vectorstore'] = None
if 'files_processed' not in st.session_state:
    st.session_state['files_processed'] = False

with st.sidebar:
    if api_key := st.text_input("Insert your API Key", type="password"):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

        session_id = st.text_input("Session ID", value="default_session")

        if 'store' not in st.session_state:
            st.session_state['store'] = {}

        uploaded_files = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=True)

        if process := st.button("Process", use_container_width=True, type="primary") and uploaded_files:
            with st.spinner("Processing..."):
                documents = []
                for file in uploaded_files:
                    temp_pdf = "./temp.pdf"
                    with open(temp_pdf, "wb") as f:
                        f.write(file.getvalue())

                    docs = PyPDFLoader(temp_pdf).load()
                    documents.extend(docs)
                
                doc_chunks = split_documents(documents)
                st.session_state.vectorstore = get_vectorstore(doc_chunks)
                st.success("Vectorstore created!")
            st.session_state.files_processed = True

if st.session_state.files_processed:
    if question := st.text_input("Ask your question:"):
        with st.spinner("Thinking..."):
            rag_chain = get_rag_qa_chain(st.session_state.vectorstore)
            response = get_conversational_rag_chain(rag_chain, question, session_id)
            st.write("**Assistant:**", response)

        with st.expander("Chat History"):
            session_history = get_session_history(session_id)
            st.write(session_history.messages)
        
else:
    st.info("Upload PDF file(s) and click 'Process' to get started")
