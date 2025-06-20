import os
from langchain_google_genai import ChatGoogleGenerativeAI

def load_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing in Streamlit secrets or environment.")
    
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.7)
