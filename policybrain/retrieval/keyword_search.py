from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def keyword_search(query: str, chunks, top_k=3):
    texts = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf = vectorizer.fit_transform(texts)
    query_vec = vectorizer.transform([query])

    scores = (tfidf @ query_vec.T).toarray().flatten()
    top_indices = scores.argsort()[-top_k:][::-1]

    return [chunks[i] for i in top_indices if scores[i] > 0]

