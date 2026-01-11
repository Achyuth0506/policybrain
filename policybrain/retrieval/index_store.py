import faiss
import pickle
import os
import numpy as np
from retrieval.vector_index import embed

CACHE_DIR = "cache"
INDEX_PATH = os.path.join(CACHE_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(CACHE_DIR, "chunks.pkl")


def load_or_build_index(chunks):
    os.makedirs(CACHE_DIR, exist_ok=True)

    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            stored_chunks = pickle.load(f)
        return index, stored_chunks

    vectors = [embed(c["text"]) for c in chunks]
    dim = len(vectors[0])

    index = faiss.IndexFlatL2(dim)
    index.add(np.vstack(vectors))

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    return index, chunks

