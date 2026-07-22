from sentence_transformers import util
from backend.constants import KEYWORDS
from backend.embeddings import get_st_model

# Precompute embeddings for each keyword category
_model = get_st_model()
KB_EMB = {cat: _model.encode(items, convert_to_tensor=True) for cat, items in KEYWORDS.items()}

def extract_agri_entities(query, similarity_threshold=0.55, max_entities_per_cat=3):
    query_emb = _model.encode(query, convert_to_tensor=True)
    entities = []
    for cat, emb in KB_EMB.items():
        scores = util.cos_sim(query_emb, emb)[0]
        sorted_idx = scores.argsort(descending=True)
        count = 0
        for idx in sorted_idx:
            score = scores[idx].item()
            if score >= similarity_threshold or count < 1:
                entities.append({"entity": cat, "value": KEYWORDS[cat][idx], "score": score})
                count += 1
            if count >= max_entities_per_cat:
                break
    entities = sorted(entities, key=lambda x: x["score"], reverse=True)
    for e in entities:
        e.pop("score", None)
    if not entities:
        entities.append({"entity": "unknown_agri", "value": query})
    return entities