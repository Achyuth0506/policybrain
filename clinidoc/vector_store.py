import faiss
import numpy as np
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔒 Simple in-memory embedding cache
_embedding_cache = {}


def embed_text(text: str) -> np.ndarray:
    if text in _embedding_cache:
        return _embedding_cache[text]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    vector = np.array(response.data[0].embedding, dtype="float32")
    _embedding_cache[text] = vector
    return vector


def build_index(documents: list[str]):
    """
    Build a FAISS index from a list of documents.
    """
    vectors = [embed_text(doc) for doc in documents]
    dim = len(vectors[0])

    index = faiss.IndexFlatL2(dim)
    index.add(np.vstack(vectors))

    return index, documents


