from pathlib import Path
from ingestion.chunker import chunk_policy

def load_policy_chunks(policy_dir="data/policies"):
    all_chunks = []

    for path in Path(policy_dir).glob("*.txt"):
        text = path.read_text()
        source = path.stem

        chunks = chunk_policy(text, source)
        all_chunks.extend(chunks)

    return all_chunks

