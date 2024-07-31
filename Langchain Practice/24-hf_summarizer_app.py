import streamlit as st
import validators,os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, WebBaseLoader

# Streamlit App
st.set_page_config(page_icon="🔗", page_title="Summarize URL")
st.title(":blue[Summarize URL] (Youtube Video or Any Web Page)")

url = st.text_input("Enter URL")

prompt_template = """
Provide a summary of the following content in proper markdown:
Content: {text}
"""
with st.sidebar:
    hf_api_token = st.text_input("Enter API Key", type="password", key="key")

if hf_api_token:
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1, huggingfacehub_api_token=hf_api_token)
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
else:
    st.info("Please enter Your HuggingFace API token")