from retrieval.index_store import load_or_build_index
from retrieval.keyword_search import keyword_search
from retrieval.vector_index import embed
import numpy as np

_vector_index = None
_chunks = None


def init_index(chunks):
    global _vector_index, _chunks
    if _vector_index is None:
        _vector_index, _chunks = load_or_build_index(chunks)


def hybrid_search(query: str, chunks, top_k=3):
    init_index(chunks)

    q_vec = embed(query)
    distances, indices = _vector_index.search(
        np.array([q_vec]), top_k
    )

    vector_hits = [_chunks[i] for i in indices[0]]
    keyword_hits = keyword_search(query, chunks, top_k)

    seen = {}
    for c in vector_hits + keyword_hits:
        seen[c["chunk_id"]] = c

    return list(seen.values())

