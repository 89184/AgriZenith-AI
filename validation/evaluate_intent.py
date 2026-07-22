#!/usr/bin/env python3
"""
Evaluate intent classification accuracy on the test set.
Computes accuracy, precision, recall, F1 per intent.
"""

import sys
import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.intent_classifier import classify_intent_hybrid

def main():
    # Read from parent directory
    input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "test_questions_100.csv")
    
    if not os.path.exists(input_path):
        print(f" {input_path} not found. Run generate_100_questions.py first.")
        return
    
    df = pd.read_csv(input_path)
    y_true = df["intent"].tolist()
    y_pred = []
    
    print("🔍 Classifying 100 questions...")
    for q in df["query"]:
        intent, _ = classify_intent_hybrid(q)
        y_pred.append(intent)
    
    print("\n Classification Report:")
    print(classification_report(y_true, y_pred))
    
    print("\n Confusion Matrix:")
    cm = pd.DataFrame(confusion_matrix(y_true, y_pred),
                      index=sorted(set(y_true)),
                      columns=sorted(set(y_true)))
    print(cm)
    
    # Save results to parent directory
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "test_results_100.csv")
    df["predicted_intent"] = y_pred
    df.to_csv(output_path, index=False)
    print(f"\n Results saved to {output_path}")

if __name__ == "__main__":
    main()