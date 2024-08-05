from crewai_tools import YoutubeChannelSearchTool
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY']= os.getenv("GROQ_API_KEY")
os.environ['OPENAI_MODEL_NAME']= 'llama3-8b-8192'
os.environ['OPENAI_API_BASE']= "https://api.groq.com/openai/v1"
# Initialize the tool with a specific Youtube channel handle to target your search
yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@FurqanQureshiBlogs',
                                   )

