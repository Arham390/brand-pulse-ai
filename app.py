import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Brand Pluse AI", layout="wide")

st.title("Brand Pluse AI")
st.markdown("Real-time semantic analysis of brand sentiment on Reddit.")

# SIDEBAR
st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Clustered Data", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to read CSV: {e}")
        st.stop()
else:
    # DEV fallback: load local CSV if present to avoid having to upload every run
    import os
    local_path = "Toyota_clustered.csv"
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
        st.sidebar.info(f"Loaded local file: {local_path}")
    else:
        st.sidebar.info("Please upload a CSV file to proceed.")
        st.stop()

# DEBUG: inspect df to diagnose "object of type 'module' has no len()" errors
st.write("DEBUG: type(df):", type(df))
st.write("DEBUG: df.shape:", getattr(df, "shape", None))
st.write("DEBUG: df.columns:", df.columns.tolist())

# TOP METRICS (guard for missing columns)
if not isinstance(df, pd.DataFrame):
    st.error("Uploaded object is not a pandas DataFrame. Make sure you used the sidebar file uploader and uploaded a CSV.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Negative Mentions", int(len(df)))
clusters_count = int(df['cluster'].nunique()) if 'cluster' in df.columns else 0
col2.metric("Crisis Clusters Detected", clusters_count)
avg_score = round(df['sentiment_score'].mean(), 2) if 'sentiment_score' in df.columns else "N/A"
col3.metric("Avg Severity Score", avg_score)

st.divider()

# VISUALIZATION: CLUSTER DISTRIBUTION
st.subheader("🔍 Identified Crisis Topics")
if 'cluster' in df.columns:
    cluster_counts = df['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster ID', 'Count']
    fig = px.bar(cluster_counts, x='Cluster ID', y='Count',
                 color='Cluster ID', title="Volume of Complaints by Topic",
                 labels={'Count': 'Number of Posts', 'Cluster ID': 'Topic Group'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No 'cluster' column found in uploaded CSV.")

# DRILL DOWN: VIEW RAW DATA
st.subheader("📝 Live Incident Feed")
if 'cluster' in df.columns:
    options = sorted(df['cluster'].unique().tolist())
    selected_cluster = st.selectbox("Filter by Cluster Topic", options=options)
    filtered_df = df[df['cluster'] == selected_cluster]
    for _, row in filtered_df.iterrows():
        excerpt = (str(row.get('text', ''))[:80] + '...') if pd.notna(row.get('text', None)) else "[no text]"
        score = round(row.get('sentiment_score', 0), 2) if pd.notna(row.get('sentiment_score', None)) else "N/A"
        with st.expander(f"🔴 [{score}] {excerpt}"):
            st.write(f"**Full Text:** {row.get('text', '')}")
            st.write(f"**Date:** {row.get('date', '')}")
            if pd.notna(row.get('url', None)) and row.get('url', ''):
                st.write(f"[View on Reddit]({row.get('url')})")
else:
    st.info("Upload a CSV with a 'cluster' column to use the drill-down.")

