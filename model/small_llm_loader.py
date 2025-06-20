import os
from langchain_openai import ChatOpenAI

# For local development only — loads .env file
if os.getenv("OPENAI_API_KEY") is None:
    from dotenv import load_dotenv
    from pathlib import Path
    load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')

def load_llm():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing. Make sure it's set in Streamlit secrets or .env.")

    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key
    )
