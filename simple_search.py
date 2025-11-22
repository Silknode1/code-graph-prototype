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

def tokenize(text):
    """Simple tokenizer: lowercase and remove non-alphanumeric characters."""
    return re.findall(r'\b\w+\b', text.lower())

def compute_tf(text):
    """Compute Term Frequency (TF)."""
    tokens = tokenize(text)
    if not tokens:
        return {}
    word_counts = Counter(tokens)
    total_words = len(tokens)
    return {word: count / total_words for word, count in word_counts.items()}

def compute_idf(documents):
    """Compute Inverse Document Frequency (IDF)."""
    N = len(documents)
    idf = {}
    all_words = set()
    
    for doc in documents:
        text = doc['skill_signal'] + " " + doc['context']
        tokens = set(tokenize(text))
        all_words.update(tokens)
        for word in tokens:
            idf[word] = idf.get(word, 0) + 1
            
    for word in all_words:
        idf[word] = math.log(N / (idf[word] + 1)) # +1 smoothing
        
    return idf

def compute_tfidf(doc, idf):
    """Compute TF-IDF vector for a document."""
    text = doc['skill_signal'] + " " + doc['context']
    tf = compute_tf(text)
    tfidf = {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}
    return tfidf

def cosine_similarity(vec1, vec2):
    """Compute Cosine Similarity between two TF-IDF vectors."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    return numerator / denominator

# --- Build Index ---
print("⚙️  Building Search Index...")
IDF_INDEX = compute_idf(DOCUMENTS)
DOC_VECTORS = [compute_tfidf(doc, IDF_INDEX) for doc in DOCUMENTS]
print(f"✅ Indexed {len(DOCUMENTS)} documents.")

def search(query, top_k=3):
    """Search for documents matching the query."""
    print(f"\n🔎 Searching for: '{query}'")
    
    # Convert query to TF-IDF vector
    query_tf = compute_tf(query)
    query_vec = {word: tf_val * IDF_INDEX.get(word, 0) for word, tf_val in query_tf.items()}
    
    results = []
    for i, doc_vec in enumerate(DOC_VECTORS):
        score = cosine_similarity(query_vec, doc_vec)
        if score > 0:
            results.append((score, DOCUMENTS[i]))
            
    # Sort by score
    results.sort(key=lambda x: x[0], reverse=True)
    
    return results[:top_k]

if __name__ == "__main__":
    # Example Queries
    queries = ["fix", "support", "optimization", "bug"] 
    
    for q in queries:
        hits = search(q)
        if hits:
            for score, doc in hits:
                print(f"   [{score:.4f}] {doc['skill_signal']} (by {doc['author']})")
        else:
            print("   No results found.")
