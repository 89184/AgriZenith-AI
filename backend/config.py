# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "farmer-advisory")
HF_TOKEN = os.getenv("HF_TOKEN")
PINECONE_DIMENSION = int(os.getenv("PINECONE_DIMENSION", 384))
PINECONE_METRIC = os.getenv("PINECONE_METRIC", "cosine")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Data
DATA_PATH = os.getenv("DATA_PATH", "./data")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

# Embedding model
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")