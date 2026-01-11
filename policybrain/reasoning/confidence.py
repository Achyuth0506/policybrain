def calibrate_confidence(
    llm_confidence: float,
    evidence_chunks: list,
    multi_hop_used: bool,
    question: str
) -> float:
    """
    Adjust confidence based on evidence quality and question clarity.
    """

    confidence = llm_confidence

    # Penalize weak evidence
    if len(evidence_chunks) < 2:
        confidence -= 0.3

    sources = {c["source"] for c in evidence_chunks}
    if len(sources) < 2:
        confidence -= 0.2

    # Penalize uncertainty introduced by multi-hop
    if multi_hop_used:
        confidence -= 0.1

   
    # Penalize vague questions (hard cap)
    vague_terms = ["allowed", "okay", "permitted", "possible"]
    if any(term in question.lower() for term in vague_terms):
        confidence = min(confidence - 0.2, 0.5)


    # Clamp
    confidence = max(0.0, min(confidence, 1.0))

    return round(confidence, 2)

