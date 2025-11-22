import urllib.request
import json
import ssl
from datetime import datetime

# Configuration
REPO = "llvm/llvm-project"  # The "High Signal" target
LIMIT = 10  # Keep it small for no-auth rate limits

def fetch_high_signal_prs():
    """
    Fetches recently merged PRs from a high-signal repo using standard library.
    """
    url = f"https://api.github.com/repos/{REPO}/pulls?state=closed&sort=updated&direction=desc&per_page={LIMIT}"
    
    print(f"🔍 Fetching last {LIMIT} closed PRs from {REPO}...")
    
    try:
        # Create a context to handle SSL (sometimes needed in restricted envs)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Python-Urllib-Client') # GitHub requires User-Agent
        
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status != 200:
                print(f"❌ Error: API returned status {response.status}")
                return []
            
            data = response.read()
            prs = json.loads(data)
        
        high_signal_data = []
        
        for pr in prs:
            # Filter for actually merged PRs
            if pr.get("merged_at"):
                author = pr["user"]["login"]
                title = pr["title"]
                body = pr["body"] or ""
                merged_at = pr["merged_at"]
                diff_url = pr["diff_url"]
                
                high_signal_data.append({
                    "author": author,
                    "skill_signal": title,
                    "context": body[:100] + "..." if len(body) > 100 else body,
                    "merged_at": merged_at,
                    "proof_url": diff_url
                })
                
        return high_signal_data

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []

if __name__ == "__main__":
    data = fetch_high_signal_prs()
    
    if data:
        print(f"\n✅ Found {len(data)} Merged PRs (Proof of Work):\n")
        for item in data:
            print(f"👤 User: {item['author']}")
            print(f"🛠  Work: {item['skill_signal']}")
            print(f"🔗 Proof: {item['proof_url']}")
            print("-" * 40)
            
        # Save to a JSON file to simulate "Ingestion"
        with open("ingested_data.json", "w") as f:
            json.dump(data, f, indent=2)
        print("\n💾 Data saved to ingested_data.json")
    else:
        print("No data found or error occurred.")
