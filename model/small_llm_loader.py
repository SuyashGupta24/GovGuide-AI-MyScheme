import os
import streamlit as st
from langchain_openai import ChatOpenAI

def load_llm():
    # Try from environment first, then from streamlit secrets
    openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing. Set it in environment or Streamlit secrets.")

    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key  # ✅ no 'proxies' param!
    )
