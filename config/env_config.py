import os
from dotenv import load_dotenv
from pathlib import Path


dir_path = (Path(__file__) /".." / "..").resolve()
env_path = os.path.join(dir_path, ".env")

load_dotenv(env_path)

# Accessing environment variables
class Environment:
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    ELEVEN_LAB_API_KEY = os.environ.get('ELEVEN_LAB_API_KEY')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


    
envs = Environment()