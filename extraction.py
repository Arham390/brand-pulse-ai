import requests
import pandas as pd
import time
from datetime import datetime
from transformers import pipeline
import sys

# Ensure console uses UTF-8 on Windows to avoid UnicodeEncodeError when printing
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    # Older/alternate streams may not support reconfigure; ignore in that case
    pass

# 1. CONFIGURATION
# 1. CONFIGURATION
TARGET_BRAND = "Toyota"
# We can search multiple subreddits by joining them with a '+'
SUBREDDIT = "toyota+ToyotaTacoma+4Runner" 
LIMIT = 300


# 2. LOAD AI MODEL (Free & Local)
print(" Loading AI Model...")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def fetch_reddit_json(subreddit, limit=25):
    """
    Fetches posts using the public .json endpoint (The YARS method).
    No API Keys needed.
    """
    # Reddit blocks requests without a User-Agent, so we fake one.
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    
    print(f" Requesting: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        print(" Rate limited! Reddit is blocking us. Try again in a few minutes.")
        return []
    if response.status_code != 200:
        print(f" Error: {response.status_code}")
        return []
        
    data = response.json()
    return data['data']['children']

def run_monitor():
    posts_data = []
    raw_posts = fetch_reddit_json(SUBREDDIT, LIMIT)
    
    print(f"Analyzing {len(raw_posts)} posts for '{TARGET_BRAND}'...")

    for entry in raw_posts:
        post = entry['data']
        
        # Combine title and text
        text_content = f"{post['title']} {post.get('selftext', '')}"
        
        # Only analyze if the brand is actually mentioned (since we are scraping a subreddit)
        if TARGET_BRAND.lower() not in text_content.lower():
            continue
            
        # Truncate for AI model
        text_content = text_content[:512]

        # --- AI SENTIMENT ANALYSIS ---
        result = sentiment_pipeline(text_content)[0]
        label = result['label']
        score = result['score']
        
        # Filter for NEGATIVE sentiment (Crisis detection)
        if label == 'NEGATIVE' and score > 0.6:
            print(f" ALERT: {post['title'][:50]}...")
            
            posts_data.append({
                "date": datetime.fromtimestamp(post['created_utc']),
                "brand": TARGET_BRAND,
                "sentiment_score": round(score, 4),
                "text": text_content,
                "url": f"https://reddit.com{post['permalink']}"
            })
            
    # SAVE TO CSV
    if posts_data:
        df = pd.DataFrame(posts_data)
        filename = f"{TARGET_BRAND}_crisis_data.csv"
        
        # Append logic
        import os
        header = not os.path.exists(filename)
        df.to_csv(filename, mode='a', header=header, index=False)
        print(f"\n Saved {len(df)} negative posts to {filename}")
    else:
        print("\n No negative posts found in this batch.")

if __name__ == "__main__":
    run_monitor()