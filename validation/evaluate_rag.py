#!/usr/bin/env python3
"""
Test RAG responses for a subset of questions.
Saves answers to a CSV for manual review.
Includes rate-limit handling with exponential backoff.
"""

import sys
import os
import time
import pandas as pd
from groq import RateLimitError

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline import farmer_advisory

def call_with_retry(query, max_retries=5, base_delay=2):
    """Call farmer_advisory with exponential backoff on rate limit errors."""
    for attempt in range(max_retries):
        try:
            return farmer_advisory(query)
        except RateLimitError as e:
            wait_time = base_delay * (2 ** attempt)  # 2, 4, 8, 16, 32 seconds
            print(f"  ⏳ Rate limit hit. Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"  Error: {e}")
            return None
    print(f"  Failed after {max_retries} retries.")
    return None

def main():
    input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "test_questions_100.csv")
    
    if not os.path.exists(input_path):
        print(f" {input_path} not found. Run generate_100_questions.py first.")
        return
    
    df = pd.read_csv(input_path).sample(20, random_state=42)
    results = []
    
    print(" Generating answers for 20 sample questions...")
    print("   (Rate limit: ~2s delay between requests)")
    
    for idx, row in df.iterrows():
        q = row["query"]
        print(f"  [{idx+1}/20] Processing: {q[:50]}...")
        
        resp = call_with_retry(q)
        
        if resp is None:
            results.append({
                "query": q,
                "expected_intent": row["intent"],
                "predicted_intent": "ERROR",
                "retrieval_confidence": 0,
                "answer": "Failed due to API error.",
            })
        else:
            results.append({
                "query": q,
                "expected_intent": row["intent"],
                "predicted_intent": resp["intent"],
                "retrieval_confidence": resp["retrieval_confidence"],
                "answer": resp["answer"],
            })
        
        # Delay between requests to avoid rate limits
        time.sleep(2)  # 2 second delay between each call
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "rag_sample_review.csv")
    out = pd.DataFrame(results)
    out.to_csv(output_path, index=False)
    print(f"\n Saved 20 sample answers to {output_path}")
    print(" Please manually review the answers for relevance and correctness.")

if __name__ == "__main__":
    main()