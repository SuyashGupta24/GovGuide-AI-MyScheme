from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Loads OPENAI_API_KEY from .env

def load_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        temperature=0.7
    )
