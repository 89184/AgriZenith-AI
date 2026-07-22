#!/usr/bin/env python3
"""
Generate 100 test questions from existing KEYWORDS and TEMPLATES.
Saves to test_questions_100.csv in the parent directory.
"""

import sys
import os
import random
import csv
from collections import Counter

# Add parent directory to path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.constants import KEYWORDS

# Your TEMPLATES
TEMPLATES = {
    "CD": [
        "What disease causes {kw}?",
        "My crop has {kw}. What is it?",
        "How to treat {kw} in plants?",
        "Symptoms of {kw}?",
        "Is {kw} a fungal or bacterial disease?",
        "What to do if I see {kw}?",
        "Can {kw} be cured?",
        "Is {kw} common in my area?",
        "How to prevent {kw}?",
    ],
    "FR": [
        "Which fertilizer is best for {kw}?",
        "What is the recommended dose of {kw} per acre?",
        "How to apply {kw} correctly?",
        "Is {kw} good for my crop?",
        "When to apply {kw}?",
        "Can I use {kw} for organic farming?",
        "What is the cost of {kw}?",
        "How does {kw} improve yield?",
    ],
    "HT": [
        "When is the right time to harvest {kw}?",
        "How do I know if {kw} is ready to harvest?",
        "What are the signs of maturity in {kw}?",
        "How many days does {kw} take to mature?",
        "Best season for harvesting {kw}?",
        "What is the ideal harvesting stage for {kw}?",
    ],
    "I": [
        "How often should I irrigate {kw}?",
        "What is the water requirement for {kw}?",
        "Which irrigation method works best for {kw}?",
        "How to schedule irrigation for {kw}?",
        "Can I use drip irrigation for {kw}?",
        "What happens if I over-irrigate {kw}?",
    ],
    "PC": [
        "How to control pests on {kw}?",
        "What is the best pesticide for {kw}?",
        "How to identify pest damage on {kw}?",
        "Are there organic ways to protect {kw} from pests?",
        "What insects attack {kw}?",
        "How to prevent pest infestation in {kw}?",
    ],
    "SM": [
        "How to improve soil health for {kw}?",
        "What is the best soil type for {kw}?",
        "How to test soil for {kw}?",
        "How to correct soil pH for {kw}?",
        "What organic matter is good for {kw}?",
        "How to prevent soil erosion in {kw} fields?",
    ],
    "M": [
        "Which machine is best for {kw}?",
        "What is the cost of {kw}?",
        "How to maintain {kw}?",
        "Can I rent {kw}?",
        "Is {kw} suitable for small farms?",
        "What are the uses of {kw}?",
    ],
    "MP": [
        "What is the current market price of {kw}?",
        "Where can I sell {kw} at best price?",
        "What is the minimum support price for {kw}?",
        "How does the price of {kw} trend?",
        "What is the wholesale rate for {kw} today?",
        "Is the price of {kw} going up or down?",
    ],
}

def generate_100_questions():
    """Generate exactly 100 questions balanced across intents."""
    all_questions = []
    intents = list(KEYWORDS.keys())
    questions_per_intent = 100 // len(intents)
    extra = 100 % len(intents)
    
    for i, intent in enumerate(intents):
        keywords = KEYWORDS[intent]
        templates = TEMPLATES[intent]
        count = questions_per_intent + (1 if i < extra else 0)
        selected_keywords = random.sample(keywords, min(count, len(keywords)))
        for kw in selected_keywords:
            template = random.choice(templates)
            question = template.format(kw=kw)
            all_questions.append({"query": question, "intent": intent})
    
    random.shuffle(all_questions)
    return all_questions[:100]

def main():
    questions = generate_100_questions()
    
    # Save to parent directory (project root)
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "test_questions_100.csv")
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["query", "intent"])
        writer.writeheader()
        writer.writerows(questions)
    
    print(f" Generated {len(questions)} questions.")
    print(f" Saved to {output_path}")

if __name__ == "__main__":
    main()