import streamlit as st
import validators,os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, WebBaseLoader

# Streamlit App
st.set_page_config(page_icon="🔗", page_title="Summarize URL")
st.title("Summarize URL (Youtube Video or Any Web Page)")

url = st.text_input("Enter URL")

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

prompt_template = """
Provide a summary of the following content in proper markdown:
Content: {text}
"""
if st.button("Summarize", type="primary"):
    if not url.strip():
        st.error("Please enter URL and API key")
    elif not validators.url(url):
        st.error("Please enter valid URL")
    else:
        try:
            with st.spinner("Summarizing..."):
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = WebBaseLoader(web_path=url)

                data = loader.load()

                prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

                chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt)

                output = chain.run(data)
                st.success(output)

        except Exception as e:
            st.error(f"An exception occurred: {e}")