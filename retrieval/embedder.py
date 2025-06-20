import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
# Config paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "processed_schemes.json")  
INDEX_DIR = os.path.join("faiss_db")
os.makedirs(INDEX_DIR, exist_ok=True)
def generate_embeddings():
    # Load schemes JSON
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        schemes = json.load(f)
    # Combine scheme fields into text with chunking
    texts = []
    for scheme in schemes:
        text = f"""
        Scheme Name: {scheme.get('scheme_name', '')}
        Ministries/Departments: {scheme.get('ministries_departments', '')}
        Target Beneficiaries: {scheme.get('target_beneficiaries', '')}
        Eligibility Criteria: {scheme.get('eligibility_criteria', '')}
        Description & Benefits: {scheme.get('details', '')} {scheme.get('benefits', '')}
        Application Process: {scheme.get('application_process', '')}
        Tags: {', '.join(scheme.get('tags', []))}
        """
        # Chunk text if too long (max 512 tokens for MiniLM)
        if len(text.split()) > 400:
            chunks = [text[i:i+400] for i in range(0, len(text), 400)]
            texts.extend(chunks)
        else:
            texts.append(text)
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    # Save FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(INDEX_DIR, "schemes.index"))
    # Save ID mapping
    with open(os.path.join(INDEX_DIR, "id2text.json"), "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
    print("[INFO] FAISS index and ID mapping created successfully!")
if __name__ == "__main__":
    generate_embeddings()
    
