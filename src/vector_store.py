import numpy as np
import json
from typing import List, Dict
import ollama

class QAVectorStore:
    def __init__(self):
        self.embeddings = []
        self.metadata = []
    
    def add_documents(self, documents: List[Dict], model: str = "nomic-embed-text"):
        """Embed QA documents using Ollama"""
        for doc in documents:
            # Generate embedding
            res = ollama.embeddings(model=model, prompt=json.dumps(doc))
            self.embeddings.append(np.array(res['embedding']))
            self.metadata.append(doc)
    
    def search(self, query: str, k: int = 3, model: str = "nomic-embed-text") -> List[Dict]:
        """Semantic search of QA documents"""
        # Embed query
        res = ollama.embeddings(model=model, prompt=query)
        query_embedding = np.array(res['embedding'])
        
        # Calculate cosine similarity
        scores = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k results
        top_indices = np.argsort(scores)[-k:][::-1]
        return [self.metadata[i] for i in top_indices] 