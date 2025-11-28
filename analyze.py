import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


filename = "Toyota_crisis_data.csv"

# load CSV into a DataFrame variable
df = pd.read_csv(filename)

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = df['text'].fillna('').astype(str).tolist()
embeddings = model.encode(texts, show_progress_bar=True)

num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)

df['cluster'] = kmeans.fit_predict(embeddings)

def get_topic_name(cluster_id):
    posts = df[df['cluster'] == cluster_id]['text']
    # Very basic "most common word" extraction
    all_text = " ".join(posts).lower().split()
    # Filter out boring words (stopwords)
    stopwords = ["the", "to", "and", "a", "of", "is", "in", "it", "for", "my", "on", "with"]
    keywords = [w for w in all_text if w not in stopwords and len(w) > 3]
    from collections import Counter
    common = Counter(keywords).most_common(3)
    return ", ".join([w[0] for w in common])
 
 
print("\n --- RESULTS ---")
for i in range(num_clusters):
    topic = get_topic_name(i)
    count = len(df[df['cluster'] == i])
    print(f" Cluster {i}: {count} posts -> Topic: [{topic}]")

# 5. SAVE FOR DASHBOARD
output_file = "Toyota_clustered.csv"
df.to_csv(output_file, index=False)
print(f"\n Saved analyzed data to '{output_file}'")
print(" Next Step: Building the Dashboard!")