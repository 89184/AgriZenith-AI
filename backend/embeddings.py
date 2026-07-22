from langchain_huggingface import HuggingFaceEmbeddings 
from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL_NAME

# LangChain embedding for retrieval
lc_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# SentenceTransformer model for intent/entity
st_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def get_lc_embeddings():
    return lc_embeddings

def get_st_model():
    return st_model