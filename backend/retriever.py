from pinecone import Pinecone
from backend.config import (
    PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME,
    PINECONE_DIMENSION, PINECONE_METRIC
)
from backend.embeddings import get_lc_embeddings

_pc = None
_index = None

def get_pinecone_index():
    global _pc, _index
    if _pc is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
    if _index is None:
        if PINECONE_INDEX_NAME not in _pc.list_indexes().names():
            _pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=PINECONE_DIMENSION,
                metric=PINECONE_METRIC
            )
        _index = _pc.Index(PINECONE_INDEX_NAME)
    return _index

def retrieve_documents(query, top_k=5):
    index = get_pinecone_index()
    embeddings = get_lc_embeddings()
    embedding = embeddings.embed_query(query)
    result = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    if not result.matches:
        return "", 0.0
    context = "\n".join(m.metadata.get("text", "") for m in result.matches)
    confidence = sum(m.score for m in result.matches) / len(result.matches)
    return context, round(confidence, 3)