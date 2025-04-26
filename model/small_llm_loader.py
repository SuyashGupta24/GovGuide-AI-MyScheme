from langchain_ollama import OllamaLLM

def load_llm():
    return OllamaLLM(model='llama3.1')  # Or 'llama3.1:7b' if you pulled a specific tag