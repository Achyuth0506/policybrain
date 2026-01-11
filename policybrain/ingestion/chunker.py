def chunk_policy(text: str, source: str, max_chars: int = 500):
    """
    Splits policy text into semantically meaningful chunks.
    Preserves source metadata for citation.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []

    for i, para in enumerate(paragraphs):
        if len(para) <= max_chars:
            chunks.append({
                "text": para,
                "source": source,
                "chunk_id": f"{source}_chunk_{i}"
            })
        else:
            for j in range(0, len(para), max_chars):
                chunks.append({
                    "text": para[j:j + max_chars],
                    "source": source,
                    "chunk_id": f"{source}_chunk_{i}_{j}"
                })

    return chunks

