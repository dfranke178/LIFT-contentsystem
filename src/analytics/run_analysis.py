#!/usr/bin/env python
"""
Script to analyze LinkedIn post data and generate statistics for the dashboard.
"""
import json
import logging
import os
from collections import Counter
from pathlib import Path
import pandas as pd
from typing import Dict, List, Any
import re
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("content_analysis")

class ContentAnalyzer:
    """Analyzes LinkedIn content and generates insights."""
    
    def __init__(self, data_dir: str = "data_store", output_dir: str = "analysis"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize storage
        self.post_data = []
        self.analysis_results = {}
    
    def load_data(self) -> bool:
        """Load post data from files."""
        try:
            posts_file = self.data_dir / "linkedin_posts.json"
            if not posts_file.exists():
                logger.warning(f"Posts file not found: {posts_file}")
                # Create an empty file if it doesn't exist
                with open(posts_file, 'w') as f:
                    json.dump([], f)
                return False
            
            with open(posts_file, 'r') as f:
                self.post_data = json.load(f)
            
            logger.info(f"Loaded {len(self.post_data)} posts")
            return len(self.post_data) > 0
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def analyze(self) -> Dict[str, Any]:
        """Run analysis on the loaded post data."""
        if not self.post_data:
            logger.warning("No data to analyze")
            return self._create_empty_analysis()
        
        # Extract basic stats
        total_posts = len(self.post_data)
        
        # Extract engagement metrics
        likes = [post.get("metrics", {}).get("likes", 0) for post in self.post_data]
        comments = [post.get("metrics", {}).get("comments", 0) for post in self.post_data]
        shares = [post.get("metrics", {}).get("shares", 0) for post in self.post_data]
        
        avg_likes = sum(likes) / total_posts if total_posts > 0 else 0
        avg_comments = sum(comments) / total_posts if total_posts > 0 else 0
        avg_shares = sum(shares) / total_posts if total_posts > 0 else 0
        
        # Analyze content types
        content_types = [post.get("content_type", "unknown").lower() for post in self.post_data]
        content_type_counter = Counter(content_types)
        
        # Extract topics using simple keyword extraction
        topics = []
        for post in self.post_data:
            content = post.get("content", "")
            if content:
                # Simple extraction of topics using keywords
                words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
                topics.extend([w for w in words if w not in self._get_stopwords()])
        
        topic_counter = Counter(topics)
        
        # Calculate engagement scores and identify top posts
        posts_with_scores = []
        for post in self.post_data:
            engagement = post.get("metrics", {})
            score = engagement.get("likes", 0) + 2 * engagement.get("comments", 0) + 3 * engagement.get("shares", 0)
            posts_with_scores.append({
                "post_id": post.get("post_id", "unknown"),
                "content": post.get("content", ""),
                "content_type": post.get("content_type", "unknown"),
                "likes": engagement.get("likes", 0),
                "comments": engagement.get("comments", 0),
                "shares": engagement.get("shares", 0),
                "engagement_score": score
            })
        
        # Sort posts by engagement score
        top_posts = sorted(posts_with_scores, key=lambda x: x["engagement_score"], reverse=True)[:5]
        
        # Add rank to top posts
        for i, post in enumerate(top_posts):
            post["rank"] = i + 1
        
        # Calculate success rates by content type
        success_rates = []
        for content_type, count in content_type_counter.items():
            if count > 0:
                # A post is successful if it has above-average engagement
                successful_posts = sum(1 for post in self.post_data 
                    if post.get("content_type", "").lower() == content_type
                    and (post.get("metrics", {}).get("likes", 0) > avg_likes 
                         or post.get("metrics", {}).get("comments", 0) > avg_comments))
                
                success_rate = (successful_posts / count) * 100
                success_rates.append({
                    "content_type": content_type,
                    "total_posts": count,
                    "successful_posts": successful_posts,
                    "success_rate": success_rate
                })
        
        # Compile analysis results
        self.analysis_results = {
            "total_posts": total_posts,
            "average_engagement": {
                "likes": avg_likes,
                "comments": avg_comments,
                "shares": avg_shares
            },
            "content_type_distribution": content_type_counter,
            "top_topics": topic_counter.most_common(20),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Save top posts data
        top_posts_df = pd.DataFrame(top_posts)
        if not top_posts_df.empty:
            top_posts_df.to_csv(self.output_dir / "top_posts.csv", index=False)
        
        # Save success rates data
        success_rates_df = pd.DataFrame(success_rates)
        if not success_rates_df.empty:
            success_rates_df.to_csv(self.output_dir / "success_rates.csv", index=False)
        
        return self.analysis_results
    
    def save_analysis(self) -> None:
        """Save analysis results to JSON file."""
        if not self.analysis_results:
            logger.warning("No analysis results to save")
            return
        
        try:
            output_file = self.output_dir / "analysis_results.json"
            with open(output_file, 'w') as f:
                json.dump(self.analysis_results, f, indent=2)
            logger.info(f"Analysis saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
    
    def _create_empty_analysis(self) -> Dict[str, Any]:
        """Create an empty analysis result for when no data is available."""
        return {
            "total_posts": 0,
            "average_engagement": {"likes": 0, "comments": 0, "shares": 0},
            "content_type_distribution": {},
            "top_topics": [],
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _get_stopwords(self) -> List[str]:
        """Return a list of stopwords to exclude from topic analysis."""
        return [
            "this", "that", "these", "those", "with", "from", "have", "has",
            "their", "they", "them", "your", "what", "when", "where", "which",
            "while", "will", "would", "could", "should", "about", "there",
            "here", "been", "being", "were", "some", "such", "than", "then",
            "only", "very", "just", "more", "most", "much", "also"
        ]

def run_analysis():
    """Run the content analysis and save results."""
    logger.info("Starting content analysis")
    
    analyzer = ContentAnalyzer()
    if analyzer.load_data():
        analyzer.analyze()
        analyzer.save_analysis()
        logger.info("Analysis completed successfully")
    else:
        logger.warning("Creating placeholder analysis results (no data)")
        analyzer.analysis_results = analyzer._create_empty_analysis()
        analyzer.save_analysis()

if __name__ == "__main__":
    run_analysis() 