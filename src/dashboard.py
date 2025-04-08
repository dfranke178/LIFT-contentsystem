import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Set page config
st.set_page_config(
    page_title="LIFT Content Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def load_analysis_data():
    """Load the analysis data from JSON file."""
    try:
        analysis_path = Path("analysis/analysis_results.json")
        if not analysis_path.exists():
            st.error("Analysis data not found. Please run the analysis script first.")
            return None
        
        with open(analysis_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading analysis data: {str(e)}")
        return None

def load_top_posts():
    """Load the top posts data from CSV file."""
    try:
        top_posts_path = Path("analysis/top_posts.csv")
        if not top_posts_path.exists():
            return None
        return pd.read_csv(top_posts_path)
    except Exception as e:
        st.error(f"Error loading top posts: {str(e)}")
        return None

def load_success_rates():
    """Load the success rates data from CSV file."""
    try:
        success_rates_path = Path("analysis/success_rates.csv")
        if not success_rates_path.exists():
            return None
        return pd.read_csv(success_rates_path)
    except Exception as e:
        st.error(f"Error loading success rates: {str(e)}")
        return None

def main():
    st.title("📊 LIFT Content Analysis Dashboard")
    
    # Load data
    analysis_data = load_analysis_data()
    if analysis_data is None:
        return
    
    top_posts = load_top_posts()
    success_rates = load_success_rates()
    
    # Overview Metrics
    st.header("📈 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", analysis_data["total_posts"])
    
    with col2:
        avg_likes = analysis_data["average_engagement"]["likes"]
        st.metric("Average Likes", f"{avg_likes:.1f}")
    
    with col3:
        avg_comments = analysis_data["average_engagement"]["comments"]
        st.metric("Average Comments", f"{avg_comments:.1f}")
    
    with col4:
        avg_shares = analysis_data["average_engagement"]["shares"]
        st.metric("Average Shares", f"{avg_shares:.1f}")
    
    # Content Type Distribution
    st.header("📊 Content Type Distribution")
    content_types = pd.DataFrame(
        analysis_data["content_type_distribution"].most_common(),
        columns=["Content Type", "Count"]
    )
    
    fig_content = px.pie(
        content_types,
        values="Count",
        names="Content Type",
        title="Distribution of Content Types"
    )
    st.plotly_chart(fig_content, use_container_width=True)
    
    # Success Rates by Content Type
    if success_rates is not None:
        st.header("🎯 Success Rates by Content Type")
        fig_success = px.bar(
            success_rates,
            x="content_type",
            y="success_rate",
            title="Success Rate by Content Type",
            labels={"content_type": "Content Type", "success_rate": "Success Rate (%)"}
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    # Top Performing Posts
    if top_posts is not None:
        st.header("🏆 Top Performing Posts")
        
        for _, post in top_posts.iterrows():
            with st.expander(f"Post #{post['rank']} - Score: {post['engagement_score']}"):
                st.write("**Content:**")
                st.write(post['content'])
                st.write("**Metrics:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Likes", post['likes'])
                with col2:
                    st.metric("Comments", post['comments'])
                with col3:
                    st.metric("Shares", post['shares'])
    
    # Topic Analysis
    st.header("🔍 Topic Analysis")
    topics = pd.DataFrame(
        analysis_data["top_topics"].most_common(10),
        columns=["Topic", "Count"]
    )
    
    fig_topics = px.bar(
        topics,
        x="Topic",
        y="Count",
        title="Top 10 Topics",
        labels={"Topic": "Topic", "Count": "Number of Posts"}
    )
    st.plotly_chart(fig_topics, use_container_width=True)

if __name__ == "__main__":
    main() 