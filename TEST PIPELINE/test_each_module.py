#!/usr/bin/env python3
"""
AgriBoot Backend Validation Script
Run this to check that all components are working correctly.
"""

import sys
import os

# Ensure backend is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# 1. Configuration & Environment

print("\n[1] Checking configuration...")
from backend.config import (
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    PINECONE_INDEX_NAME,  # <-- ADDED
    GROQ_API_KEY,
    DATA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL_NAME
)

assert PINECONE_API_KEY is not None and PINECONE_API_KEY.startswith("pcsk_"), " Pinecone API key missing or invalid"
assert PINECONE_ENVIRONMENT is not None, "Pinecone environment URL missing"
assert GROQ_API_KEY is not None and GROQ_API_KEY.startswith("gsk_"), " Groq API key missing or invalid"
print(" Config loaded successfully")


# 2. Embeddings & SentenceTransformer

print("\n[2] Testing embedding models...")
from backend.embeddings import get_lc_embeddings, get_st_model

lc_emb = get_lc_embeddings()
st_model = get_st_model()
test_embed = lc_emb.embed_query("test")
assert len(test_embed) == 384, f" LangChain embedding dimension mismatch: {len(test_embed)}"
test_st_embed = st_model.encode("test")
assert len(test_st_embed) == 384, f" SentenceTransformer embedding dimension mismatch: {len(test_st_embed)}"
print(" Embedding models load and produce 384‑dim vectors")


# 3. Data Loader (optional – only if you have data in DATA_PATH)

print("\n[3] Testing data loader...")
from backend.data_loader import load_and_split_documents
try:
    docs = load_and_split_documents()
    print(f" Loaded {len(docs)} document chunks from {DATA_PATH}")
except Exception as e:
    print(f"  Data loader warning (maybe no files in {DATA_PATH}): {e}")


# 4. Pinecone Index

print("\n[4] Checking Pinecone index...")
from backend.retriever import get_pinecone_index
index = get_pinecone_index()
stats = index.describe_index_stats()
print(f" Pinecone index '{PINECONE_INDEX_NAME}' ready – {stats.total_vector_count} vectors")
assert stats.dimension == 384, " Index dimension mismatch"
assert stats.metric == "cosine", " Index metric mismatch"


# 5. Intent Classification

print("\n[5] Testing intent classification...")
from backend.intent_classifier import classify_intent_hybrid

test_queries = [
    "my wheat leaves are turning yellow",
    "best fertilizer for rice",
    "when to harvest tomatoes",
    "price of potato today",
]
for q in test_queries:
    intent, conf = classify_intent_hybrid(q)
    print(f"  Query: '{q}' → {intent} (conf={conf:.2f})")
print(" Intent classification works")


# 6. Entity Extraction

print("\n[6] Testing entity extraction...")
from backend.entity_extractor import extract_agri_entities

ents = extract_agri_entities("how to control aphids on cotton")
print(f"  Found {len(ents)} entities: {ents[:3]}...")
assert len(ents) > 0, "No entities extracted"
print(" Entity extraction works")


# 7. Retrieval (RAG)

print("\n[7] Testing document retrieval...")
from backend.retriever import retrieve_documents

context, conf = retrieve_documents("irrigation methods for maize")
print(f"  Retrieved {len(context)} characters, confidence={conf:.3f}")
if len(context) == 0:
    print("    No documents retrieved – ensure your Pinecone index has data and the query matches.")
else:
    print(" Retrieval works")


# 8. Generation (Groq)

print("\n[8] Testing LLM generation (Groq)...")
from backend.generator import generate_answer

# Use a simple query and the retrieved context (or empty)
answer = generate_answer("What is drip irrigation?", context)
print(f"  Generated answer (first 200 chars): {answer[:200]}...")
assert len(answer) > 10, "Generation returned very short answer"
print("Generation works")


# 9. Full Pipeline

print("\n[9] Testing full farmer_advisory pipeline...")
from backend.pipeline import farmer_advisory

result = farmer_advisory("how to improve soil fertility")
print(f"  Intent: {result['intent']} (conf={result['intent_confidence']})")
print(f"  Entities: {[e['entity'] for e in result['entities']]}")
print(f"  Answer (first 200 chars): {result['answer'][:200]}...")
assert "intent" in result, " Pipeline missing 'intent'"
assert "answer" in result, " Pipeline missing 'answer'"
print(" Full pipeline works")


print("\n All backend tests passed! Your system is fully functional.")