import logging
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .pdf_parser import DocumentSection

class EmbeddingProcessor:
    def __init__(self, model_name: str, top_k: int = 5):
        self.model = SentenceTransformer(model_name)
        self.top_k = top_k
        self.index = None
    
    def rank_sections(self, sections: list[DocumentSection], query: str) -> list:
        if not sections:
            return []
        
        # Prepare text embeddings
        texts = [s.text for s in sections]
        section_embeddings = self._get_embeddings(texts)
        
        # Create and search index
        self._create_index(section_embeddings)
        query_embedding = self._get_embeddings([query])
        scores, indices = self.index.search(query_embedding, len(sections))
        
        # Return sorted sections
        sorted_sections = [sections[i] for i in indices[0]]
        return sorted_sections[:self.top_k]
    
    def select_best_paragraph(self, text: str, query: str) -> str:
        paragraphs = self._split_paragraphs(text)
        if not paragraphs:
            return text[:1000] + "..." if len(text) > 1000 else text
        
        para_embeddings = self._get_embeddings(paragraphs)
        query_embedding = self._get_embeddings([query])
        
        index = faiss.IndexFlatIP(para_embeddings.shape[1])
        index.add(para_embeddings)
        _, indices = index.search(query_embedding, 1)
        
        return paragraphs[indices[0][0]]
    
    def _get_embeddings(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(
            texts, 
            convert_to_numpy=True,
            show_progress_bar=False
        )
        faiss.normalize_L2(embeddings)
        return embeddings
    
    def _create_index(self, embeddings: np.ndarray):
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
    
    def _split_paragraphs(self, text: str) -> list[str]:
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        return paras or [text]