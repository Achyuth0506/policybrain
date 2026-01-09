from vector_store import embed_text, build_index
from guidelines_data import GUIDELINES
import numpy as np

_index = None
_docs = None

def get_index():
    global _index, _docs
    if _index is None:
        _index, _docs = build_index(GUIDELINES)
    return _index, _docs


def retrieve(query: str, top_k: int = 2):
    index, docs = get_index()
    query_vec = embed_text(query)

    distances, indices = index.search(
        np.array([query_vec]), top_k
    )

    return [docs[i] for i in indices[0]]

