import faiss
import numpy as np

def create_index(dim: int) -> faiss.Index:
    return faiss.IndexFlatIP(dim)

def search_index(index: faiss.Index, 
                query_embedding: np.ndarray, 
                k: int) -> Tuple[np.ndarray, np.ndarray]:
    D, I = index.search(query_embedding, k)
    return D, I