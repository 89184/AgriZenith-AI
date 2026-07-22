from textblob import TextBlob
from fuzzywuzzy import process
from transformers import pipeline
from backend.constants import KEYWORDS, ZS_INTENTS
from backend.embeddings import get_st_model

# Global zero-shot classifier (load once)
_zero_shot_classifier = None

def get_zero_shot_classifier():
    global _zero_shot_classifier
    if _zero_shot_classifier is None:
        _zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _zero_shot_classifier

def correct_spelling(query):
    return str(TextBlob(query).correct())

def fuzzy_score(query, keywords_dict):
    best_intent = None
    best_score = 0
    for intent, keywords in keywords_dict.items():
        score = max([process.extractOne(query, [kw])[1] for kw in keywords])
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent, best_score / 100.0

def embedding_score(query, keywords_dict):
    embedder = get_st_model()
    query_vec = embedder.encode(query, convert_to_tensor=True)
    best_intent = None
    best_score = 0
    for intent, keywords in keywords_dict.items():
        kw_vecs = embedder.encode(keywords, convert_to_tensor=True)
        score = max(embedder.similarity(query_vec, kw_vecs)[0]).item()
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent, best_score

def classify_intent_hybrid(query, threshold=0.4):
    query_clean = correct_spelling(query.lower())
    fuzzy_intent, fuzzy_conf = fuzzy_score(query_clean, KEYWORDS)
    embed_intent, embed_conf = embedding_score(query_clean, KEYWORDS)
    hybrid_conf = (fuzzy_conf + embed_conf) / 2
    hybrid_intent = embed_intent if embed_conf >= fuzzy_conf else fuzzy_intent

    # exact keyword match
    for intent, words in KEYWORDS.items():
        if any(word in query_clean for word in words):
            return intent, 0.95

    if hybrid_intent == "CD":
        if any(k in query_clean for k in ["price", "rate", "market", "harvest", "water",
                                          "irrigation", "machine", "tractor", "fertilizer",
                                          "soil", "pest"]):
            hybrid_conf *= 0.6

    INTENT_PRIORITY = ["MP", "HT", "M", "I", "FR", "PC", "SM", "CD"]

    if hybrid_conf >= threshold:
        for intent in INTENT_PRIORITY:
            if intent in (fuzzy_intent, embed_intent):
                return intent, round(hybrid_conf, 3)

    zs = get_zero_shot_classifier()(query_clean, list(KEYWORDS.keys()))
    return zs["labels"][0], round(zs["scores"][0], 3)