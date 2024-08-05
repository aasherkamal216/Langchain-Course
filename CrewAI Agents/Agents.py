from crewai import Agent
from Tools import yt_tool
import os, dotenv
from langchain_groq import ChatGroq

dotenv.load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-70b-versatile")

blog_researcher = Agent(
    role='Blog Researcher from Youtube Videos',
    goal='Get the relevant video transcription for the topic {topic} from the provided Youtube channel',
    verbose=True,
    memory=True,
    llm=llm,
    backstory=(
       "Expert in understanding videos about Universe, Angels, History and Religion" 
    ),
    tools=[yt_tool],
    allow_delegation=True,
    embedder={
            "provider": "google",
            "config":{
                "model": 'models/embedding-001',
                "task_type": "retrieval_document",
                "title": "Embeddings for Embedchain"
            }
        }
)

# Creating a senior blog writer agent with YT tool

blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate interesting stories about the video {topic} from YT video',
    verbose=True,
    memory=True,
    llm=llm,
    backstory=(
        """Expert in simplifying complex topics, crafting
        engaging narratives that captivate and educate, in an easy manner."""
    ),
    tools=[yt_tool],
    allow_delegation=False,
    embedder={
            "provider": "google",
            "config":{
                "model": 'models/embedding-001',
                "task_type": "retrieval_document",
                "title": "Embeddings for Embedchain"
            }
        }
)