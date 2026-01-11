from retrieval.hybrid_search import hybrid_search
from retrieval.query_rewriter import rewrite_query

DEPENDENCY_KEYWORDS = [
    "provided that",
    "if",
    "must",
    "requires",
    "requirement",
    "as defined",
    "subject to"
]


def needs_follow_up(evidence_chunks):
    """
    Detect whether retrieved evidence implies additional dependencies.
    """
    for c in evidence_chunks:
        text = c["text"].lower()
        for kw in DEPENDENCY_KEYWORDS:
            if kw in text:
                return True
    return False


def generate_follow_up_query(original_query, evidence_chunks):
    """
    Generate a refined query to resolve policy dependencies.
    """
    context = " ".join(c["text"] for c in evidence_chunks)

    follow_up_prompt = f"""
Given the following healthcare policy excerpts:

{context}

Identify what additional policy conditions or definitions are required
to fully answer the original question:

{original_query}

Return only a short search query.
"""

    return rewrite_query(follow_up_prompt)


def multi_hop_retrieve(user_query, chunks, top_k=3):
    """
    Perform initial retrieval and optional follow-up retrieval.
    Returns: (evidence_chunks, multi_hop_used)
    """
    rewritten = rewrite_query(user_query)
    initial_hits = hybrid_search(rewritten, chunks, top_k)

    if not needs_follow_up(initial_hits):
        return initial_hits, False

    follow_up_query = generate_follow_up_query(user_query, initial_hits)
    follow_up_hits = hybrid_search(follow_up_query, chunks, top_k)

    seen = {}
    for c in initial_hits + follow_up_hits:
        seen[c["chunk_id"]] = c

    return list(seen.values()), True

