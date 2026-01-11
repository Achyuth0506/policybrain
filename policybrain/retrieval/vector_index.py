import faiss
import numpy as np
import os
import pickle
from openai import OpenAI

CACHE_DIR = "cache"
EMBEDDING_CACHE_PATH = os.path.join(CACHE_DIR, "embeddings.pkl")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load embedding cache
if os.path.exists(EMBEDDING_CACHE_PATH):
    with open(EMBEDDING_CACHE_PATH, "rb") as f:
        _embedding_cache = pickle.load(f)
else:
    _embedding_cache = {}


def embed(text: str) -> np.ndarray:
    if text in _embedding_cache:
        return _embedding_cache[text]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    vec = np.array(response.data[0].embedding, dtype="float32")
    _embedding_cache[text] = vec

    # Persist cache
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(EMBEDDING_CACHE_PATH, "wb") as f:
        pickle.dump(_embedding_cache, f)

    return vec

