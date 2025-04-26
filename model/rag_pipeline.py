import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from retrieval.retriever import SchemeRetriever
from model.small_llm_loader import load_llm
from langchain_core.prompts import ChatPromptTemplate

retriever = SchemeRetriever()
llm = load_llm()

def generate_answer(question):
    # Retrieve documents
    docs = retriever.retrieve(question)

    context = "\n\n".join(docs)

    # Enhanced prompt template
    prompt_template = ChatPromptTemplate.from_template(
        """
        You are an expert on Indian government schemes. Based on the following scheme details, provide a concise and accurate answer to the user's question. If the information is insufficient, state so clearly.

        **Context**:
        {context}

        **Question**:
        {question}

        **Instructions**:
        - Answer in a clear, structured format.
        - If specific schemes are relevant, list them by name.
        - If no schemes match, suggest checking official sources like myscheme.gov.in.
        """
    )
    chain = prompt_template | llm

    # Run
    try:
        response = chain.invoke({"context": context, "question": question})
        return response
    except Exception as e:
        return f"Error generating answer: {str(e)}"

