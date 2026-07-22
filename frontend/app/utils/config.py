import os
from dotenv import load_dotenv

load_dotenv()  # Load .env from project root

API_URL = os.getenv("API_URL", "http://localhost:8000")