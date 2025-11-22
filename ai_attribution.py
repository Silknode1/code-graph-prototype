import json
import math
import re
from collections import Counter

# Load the ingested data
try:
    with open("ingested_data.json", "r") as f:
        DOCUMENTS = json.load(f)
except FileNotFoundError:
    print("❌ Error: ingested_data.json not found. Run github_fetcher.py first.")
    exit(1)

def calculate_entropy(text):
    """
    Calculates Shannon Entropy of the text.
    Higher entropy -> More unpredictable (often Human).
    Lower entropy -> More predictable (often AI/Boilerplate).
    """
    if not text:
        return 0
    
    # Normalize slightly to avoid noise
    text = text.lower()
    
    # Count character frequencies
    counts = Counter(text)
    total_chars = len(text)
    
    entropy = 0
    for count in counts.values():
        p = count / total_chars
        entropy -= p * math.log2(p)
        
    return entropy

def analyze_structure(text):
    """
    Analyzes code structure for 'AI-like' patterns.
    - AI tends to over-comment.
    - AI tends to write very uniform line lengths.
    """
    lines = text.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    
    if not non_empty_lines:
        return 0, 0
    
    # 1. Comment Density (Heuristic: AI explains everything)
    comment_lines = [l for l in non_empty_lines if l.strip().startswith(('#', '//', '*', '/*'))]
    comment_ratio = len(comment_lines) / len(non_empty_lines)
    
    # 2. Line Length Variance (Heuristic: AI is uniform, Humans are chaotic)
    lengths = [len(l) for l in non_empty_lines]
    avg_len = sum(lengths) / len(lengths)
    variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    
    return comment_ratio, std_dev

def detect_ai_probability(doc):
    """
    Combines metrics into a pseudo-probability score.
    THIS IS A PROTOTYPE HEURISTIC.
    """
    # We analyze the 'context' (the PR body) and the 'skill_signal' (Title)
    # In a real app, we'd analyze the raw diff content.
    content = doc['context'] + "\n" + doc['skill_signal']
    
    entropy = calculate_entropy(content)
    comment_ratio, std_dev = analyze_structure(content)
    
    # Heuristic Logic:
    # - Low Entropy (< 4.0) + High Comment Ratio (> 0.3) -> Likely AI
    # - High Entropy (> 4.5) + High Variance (> 20) -> Likely Human (Chaotic/Novel)
    
    ai_score = 0.0
    
    # Entropy Penalty (AI is predictable)
    if entropy < 4.2:
        ai_score += 0.4
    elif entropy > 4.8:
        ai_score -= 0.2
        
    # Comment Penalty (AI over-explains)
    if comment_ratio > 0.25:
        ai_score += 0.3
        
    # Variance Bonus (Humans are messy)
    if std_dev < 10: # Very uniform lines
        ai_score += 0.2
    elif std_dev > 30: # Very jagged code
        ai_score -= 0.2
        
    # Clamp to 0-1
    return max(0.0, min(1.0, ai_score)), entropy, comment_ratio, std_dev

print(f"🕵️‍♀️  Running AI Forensics on {len(DOCUMENTS)} items...\n")

print(f"{'USER':<15} | {'AI SCORE':<10} | {'ENTROPY':<8} | {'COMMENTS':<8} | {'SIGNAL'}")
print("-" * 80)

for doc in DOCUMENTS:
    score, ent, com, dev = detect_ai_probability(doc)
    
    # Colorize output
    score_str = f"{score:.2f}"
    signal = "🤖 Likely AI" if score > 0.6 else "👤 Likely Human"
    if score < 0.3: signal = "🧠 High Logic (Human)"
    
    print(f"{doc['author'][:15]:<15} | {score_str:<10} | {ent:.2f}     | {com:.2f}     | {signal}")

print("\n✅ Analysis Complete.")
