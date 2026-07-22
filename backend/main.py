# backend/main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from backend.pipeline import farmer_advisory

app = FastAPI(
    title="AgriBoot API",
    description="AI-powered farmer advisory system",
    version="1.0"
)

# Enable CORS for all origins (so desktop and mobile apps can call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    intent_confidence: float
    retrieval_confidence: float
    entities: List[dict]
    answer: str
    context: Optional[str] = ""

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Endpoint to get farming advice.
    """
    try:
        result = farmer_advisory(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "message": "AgriBoot is running"}
@app.get("/")
async def root():
    return {"message": "AgriBoot API is running. Use POST /ask to get advice."}
