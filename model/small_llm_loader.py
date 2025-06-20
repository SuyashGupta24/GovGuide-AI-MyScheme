from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  

def load_llm():
    openai_api_key = os.getenv("OPENAI_API_KEY")  
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key  
    )
