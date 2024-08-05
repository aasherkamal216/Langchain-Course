from crewai import Crew, Process
from Agents import blog_researcher, blog_writer
from Tasks import research_task, write_task
from rich import print
import os, dotenv
dotenv.load_dotenv()

# Forming the crew with some enhanced configurations
crew = Crew(
  agents=[blog_researcher, blog_writer],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=50,
  share_crew=True,
  embedder={
            "provider": "google",
            "config":{
                "model": 'models/embedding-001',
                "task_type": "retrieval_document",
                "title": "Embeddings for Embedchain"
            }
        }
)


## start the task execution process with enhanced feedback
result = crew.kickoff(inputs = {"topic":"Creation Of The Universe & Seven Skies"})
print(result)