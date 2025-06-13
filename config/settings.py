import os
from dotenv import load_dotenv

# Api keys
load_dotenv()

deepseek_api_key = os.getenv("HUGGING_FACE_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
llama3_api_key = os.getenv("GROQ_API_KEY")
