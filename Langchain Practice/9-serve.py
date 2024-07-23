import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
# llm model
llm = ChatGroq(model="llama3-8b-8192")
# prompt template
template = "Translate the following text into {language}"

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("user", "{text}")
])
# output parser
parser = StrOutputParser()
# chain
chain = prompt | llm | parser

# FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# chain routes
add_routes(
    app,
    chain,
    path="/groq"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# write 'python file_path/app_name.py' in terminal