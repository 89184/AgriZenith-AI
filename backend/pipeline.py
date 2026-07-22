from backend.intent_classifier import classify_intent_hybrid
from backend.entity_extractor import extract_agri_entities
from backend.retriever import retrieve_documents
from backend.generator import generate_answer

def rag_pipeline(query):
    intent, intent_conf = classify_intent_hybrid(query)
    entities = extract_agri_entities(query)
    context, retrieval_conf = retrieve_documents(query)
    answer = generate_answer(query, context)
    return {
        "intent": intent,
        "intent_confidence": intent_conf,
        "retrieval_confidence": retrieval_conf,
        "entities": entities,
        "answer": answer
    }

def farmer_advisory(query):
    # same as rag_pipeline but with explicit rounding (if needed)
    return rag_pipeline(query)