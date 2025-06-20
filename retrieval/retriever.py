try:
    import faiss
except ImportError:
    import faiss_cpu as faiss

import os
import json
from sentence_transformers import SentenceTransformer

INDEX_DIR = os.path.join("faiss_db")

class SchemeRetriever:
    def __init__(self):
        INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "faiss_db")
        self.index = faiss.read_index(os.path.join(INDEX_DIR, "schemes.index"))

        with open(os.path.join(INDEX_DIR, "id2text.json"), "r", encoding="utf-8") as f:
            self.id2text = json.load(f)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve(self, query, top_k=3):  # Reduced top_k for precision
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.id2text):
                results.append(self.id2text[idx])
        return results
