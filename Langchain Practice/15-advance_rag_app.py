import os, dotenv
dotenv.load_dotenv()
import streamlit as st
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Groq RAG Chatbot"
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

def get_document(file):

    temp_dir = tempfile.TemporaryDirectory()

    temp_filepath = os.path.join(temp_dir.name, file.name)
    with open(temp_filepath, "wb") as f:
        f.write(file.getvalue())
    documents = PyPDFLoader(temp_filepath).load()

    return documents

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

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def rag_qa(question, vectorstore):

    llm = ChatGroq(model="llama-3.1-70b-versatile")
    output_parser = StrOutputParser()

    contextualize_q_system_prompt = """Given a chat history and the latest user question 
        which might reference context in the chat history, formulate a standalone question 
        which can be understood without the chat history. Do NOT answer the question, 
        just reformulate it if needed and otherwise return it as is."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
    contextualize_q_chain = contextualize_q_prompt | llm | output_parser

    qa_system_prompt = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise.

    {context}"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
    
    retriever = vectorstore.as_retriever()

    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualize_q_chain | retriever | format_docs
        )
        | prompt
        | llm
        | output_parser
    )

    return rag_chain.stream({"question": question, "chat_history": st.session_state.chat_history})


## Streamlit code
st.title('Groq :green[RAG] Chatbot')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hi there! How can I assist you?")]
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# Displaying the chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

with st.sidebar:
    upload_pdf = st.file_uploader("Upload PDF file", type="pdf")

    if process := st.button("Process", use_container_width=True) and upload_pdf:

        with st.spinner("Processing..."):
            documents = get_document(upload_pdf)
            doc_chunks = split_documents(documents)
            st.session_state.vectorstore = get_vectorstore(doc_chunks)
            st.success("Vectorstore created!")
        st.session_state.file_processed = True

if st.session_state.file_processed:
    if question := st.chat_input("Ask your question"):
        st.session_state.chat_history.append(HumanMessage(content=question))
        
        with st.chat_message("Human"):
            st.write(question)

        with st.chat_message("AI"):
            response = st.write_stream(rag_qa(question, st.session_state.vectorstore))
        st.session_state.chat_history.append(AIMessage(content=response))
        
else:
    st.info("Upload a PDF file and click 'Process' to get started")

