# 📉 BrandPulse: AI-Powered Crisis Detection System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AI Model](https://img.shields.io/badge/Model-DistilBERT-orange)
![Clustering](https://img.shields.io/badge/Algorithm-HDBSCAN-green)
![Status](https://img.shields.io/badge/Status-Active_Development-brightgreen)

**BrandPulse** is a real-time intelligence tool that monitors social media (Reddit) to detect emerging PR crises before they go viral. Unlike standard sentiment analysis tools that just count "negative tweets," BrandPulse uses **semantic clustering** to identify _specific_ complaints (e.g., "Brake Failure" vs. "High Prices") and separate signal from noise.

---

## 🚀 Key Features

- **🧠 Context-Aware Sentiment Filtering:** Uses a fine-tuned **DistilBERT** transformer model to filter out noise and identify high-confidence negative sentiment.
- **🔍 Unsupervised Topic Discovery:** Implements **Sentence-BERT** embeddings and **K-Means/HDBSCAN** clustering to automatically group scattered complaints into coherent "Crisis Topics" without manual labeling.
- **🛡️ Rate-Limit Resistant:** Custom scraping engine capable of gathering data via public JSON endpoints, bypassing the need for expensive Enterprise APIs.
- **📊 Crisis Analytics:** (In Progress) Velocity tracking to detect when a specific complaint cluster is "spiking" in real-time.

---

## 🛠️ System Architecture

The pipeline consists of three main stages:

```mermaid
graph LR
    A[Data Ingestion] -->|Scrape Reddit| B(Sentiment Filter)
    B -->|DistilBERT < 0.05| C{Is it a Crisis?}
    C -->|Yes| D[Vector Embeddings]
    D -->|Sentence-Transformers| E[Semantic Clustering]
    E -->|K-Means| F[Crisis Report]
Listening Post: Scrapes raw discussions from targeted subreddits (e.g., r/Toyota, r/Tesla).

Filter Engine: Discards positive/neutral posts; keeps only high-confidence negative feedback.

Clustering Engine: Converts text to high-dimensional vectors and groups them to find common defect patterns.

💻 Tech Stack
Language: Python 3.10+

NLP & AI: Hugging Face Transformers, Sentence-Transformers

Machine Learning: Scikit-Learn (K-Means), PyTorch

Data Engineering: Pandas, Requests (Custom JSON Scraper)

⚡ Quick Start
1. Clone the Repository
Bash

git clone [https://github.com/YOUR_USERNAME/brand-pulse.git](https://github.com/YOUR_USERNAME/brand-pulse.git)
cd brand-pulse
2. Set Up Environment
It is recommended to use a virtual environment to manage dependencies.

Bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
(If you don't have a requirements.txt yet, run: pip install pandas requests transformers torch scikit-learn sentence-transformers)

4. Run the Collector
Start scraping real-time data from Reddit.

Bash

python src/collector.py
Output: Saves a CSV file (e.g., Toyota_crisis_data.csv) with negative posts.

5. Run the Analysis
Cluster the collected data into topics.

Bash

python src/cluster_analysis.py
📈 Example Output
Input: 100 raw posts about Toyota. Output:

Plaintext

🔍 --- IDENTIFIED CRISIS CLUSTERS ---

📁 CLUSTER 1: Mechanical Failures (ECU/Engine)
   - "Toyota said I need a new ECU for my 2022 Tacoma..."
   - "Check engine light came on after just 5k miles..."

📁 CLUSTER 2: Dealer & Service Issues
   - "Dealer markup is insane, they want $5k over MSRP..."
   - "Service center kept my car for 3 weeks without updates..."
🛣️ Roadmap
[x] Iteration 1: Data Collection Pipeline

[x] Iteration 2: AI Sentiment Filtering (DistilBERT)

[x] Iteration 3: Topic Clustering (K-Means)

[ ] Iteration 4: Real-time Streamlit Dashboard

[ ] Iteration 5: Automated Email Alerts

🤝 Contributing
Contributions are welcome! Please open an issue if you encounter any bugs or have feature requests.

📄 License
This project is open-source and available under the MIT License.
```
