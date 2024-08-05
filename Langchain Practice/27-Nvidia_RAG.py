import streamlit as st
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import time

from dotenv import load_dotenv
load_dotenv()

# Link: https://build.nvidia.com/explore/discover

os.environ['NVIDIA_API_KEY']=os.getenv("NVIDIA_API_KEY")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

def create_vectorstore():
    st.session_state.embeddings= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    st.session_state.loader = PyPDFLoader("Langchain Practice/National AI Policy Consultation Draft.pdf") ## Data Ingestion
    st.session_state.docs = st.session_state.loader.load() ## Document Loading
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=700,chunk_overlap=50) ## Chunk Creation
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:30]) #splitting
    st.session_state.vectorstore = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings) #vector embeddings


st.title(":green[Nvidia] NIM RAG App")
llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct")


prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)


with st.sidebar:
    st.divider()
    if st.button("Create Vectorstore", use_container_width=True, type="primary"):
        with st.spinner("Creating Vectorstore..."):
            create_vectorstore()
            st.success("Vectorstore is ready!")
    

question = st.text_input("Enter Your Question From Document", disabled=not st.session_state.vectorstore)

if question:
    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({'input': question})

    print("Response time :", time.process_time()-start)
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Retrieved Documents"):
        # Find the retrieved chunks
        for i, doc in enumerate(response["context"]):
            st.write(f"Document {i+1}:\n\n {doc.page_content}")
            st.write("----")

