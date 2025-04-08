import json
import os
import csv
from collections import Counter
from typing import Dict, List
import logging
from utils import get_posts_for_training

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_analysis(analysis: Dict, output_dir: str = "analysis") -> None:
    """
    Export analysis results to JSON and CSV files.
    
    Args:
        analysis (Dict): Analysis results to export
        output_dir (str): Directory to save the exported files
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export to JSON
        json_path = os.path.join(output_dir, "analysis_results.json")
        with open(json_path, 'w') as f:
            json.dump(analysis, f, indent=4)
        logger.info(f"Analysis results saved to {json_path}")
        
        # Export top performing posts to CSV
        csv_path = os.path.join(output_dir, "top_posts.csv")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'rank', 'content', 'engagement_score', 'likes', 
                'comments', 'shares', 'content_type'
            ])
            writer.writeheader()
            for i, post in enumerate(analysis["top_performing_posts"], 1):
                writer.writerow({
                    'rank': i,
                    'content': post['content'],
                    'engagement_score': post['engagement_score'],
                    'likes': post['likes'],
                    'comments': post['comments'],
                    'shares': post['shares'],
                    'content_type': post['content_type']
                })
        logger.info(f"Top posts saved to {csv_path}")
        
        # Export content type success rates to CSV
        success_path = os.path.join(output_dir, "success_rates.csv")
        with open(success_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'content_type', 'total_posts', 'high_success_posts', 'success_rate'
            ])
            writer.writeheader()
            for content_type, stats in analysis["success_by_content_type"].items():
                writer.writerow({
                    'content_type': content_type,
                    'total_posts': stats['total'],
                    'high_success_posts': stats['high_success'],
                    'success_rate': stats['success_rate']
                })
        logger.info(f"Success rates saved to {success_path}")
        
    except Exception as e:
        logger.error(f"Error exporting analysis: {str(e)}")
        raise

def analyze_training_data() -> Dict:
    """
    Analyze the training data and provide insights.
    
    Returns:
        Dict: Analysis results including:
        - Total number of posts
        - Distribution of content types
        - Average engagement metrics
        - Most common topics
        - Success rate by content type
        - Top performing posts
    """
    try:
        # Get the training data
        posts = get_posts_for_training()
        logger.info(f"Analyzing {len(posts)} posts")
        
        # Initialize analysis results
        analysis = {
            "total_posts": len(posts),
            "content_type_distribution": Counter(),
            "average_engagement": {
                "likes": 0,
                "comments": 0,
                "shares": 0
            },
            "top_topics": Counter(),
            "success_by_content_type": {},
            "top_performing_posts": []
        }
        
        # Calculate metrics
        total_likes = 0
        total_comments = 0
        total_shares = 0
        
        for post in posts:
            metadata = post["metadata"]
            
            # Content type distribution
            content_type = metadata["content_type"]
            analysis["content_type_distribution"][content_type] += 1
            
            # Engagement metrics
            total_likes += metadata["likes"]
            total_comments += metadata["comments"]
            total_shares += metadata["shares"]
            
            # Topic analysis
            if metadata["topic"]:
                analysis["top_topics"][metadata["topic"]] += 1
            
            # Success by content type
            if content_type not in analysis["success_by_content_type"]:
                analysis["success_by_content_type"][content_type] = {
                    "total": 0,
                    "high_success": 0
                }
            analysis["success_by_content_type"][content_type]["total"] += 1
            if metadata["success_rating"] == "high":
                analysis["success_by_content_type"][content_type]["high_success"] += 1
            
            # Track top performing posts
            engagement_score = metadata["likes"] + metadata["comments"] * 2 + metadata["shares"] * 3
            analysis["top_performing_posts"].append({
                "content": post["content"][:100] + "...",  # First 100 chars
                "engagement_score": engagement_score,
                "likes": metadata["likes"],
                "comments": metadata["comments"],
                "shares": metadata["shares"],
                "content_type": content_type
            })
        
        # Calculate averages
        analysis["average_engagement"]["likes"] = total_likes / len(posts)
        analysis["average_engagement"]["comments"] = total_comments / len(posts)
        analysis["average_engagement"]["shares"] = total_shares / len(posts)
        
        # Sort top performing posts
        analysis["top_performing_posts"].sort(key=lambda x: x["engagement_score"], reverse=True)
        analysis["top_performing_posts"] = analysis["top_performing_posts"][:5]  # Top 5 posts
        
        # Calculate success rates
        for content_type in analysis["success_by_content_type"]:
            total = analysis["success_by_content_type"][content_type]["total"]
            high_success = analysis["success_by_content_type"][content_type]["high_success"]
            analysis["success_by_content_type"][content_type]["success_rate"] = (high_success / total) * 100
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing training data: {str(e)}")
        raise

def print_analysis(analysis: Dict) -> None:
    """Print the analysis results in a readable format."""
    print("\n=== Training Data Analysis ===")
    print(f"\nTotal Posts: {analysis['total_posts']}")
    
    print("\nContent Type Distribution:")
    for content_type, count in analysis["content_type_distribution"].most_common():
        print(f"- {content_type}: {count} posts")
    
    print("\nAverage Engagement:")
    for metric, value in analysis["average_engagement"].items():
        print(f"- {metric}: {value:.2f}")
    
    print("\nTop Topics:")
    for topic, count in analysis["top_topics"].most_common(5):
        print(f"- {topic}: {count} posts")
    
    print("\nSuccess Rate by Content Type:")
    for content_type, stats in analysis["success_by_content_type"].items():
        print(f"- {content_type}: {stats['success_rate']:.1f}% high success rate")
    
    print("\nTop 5 Performing Posts:")
    for i, post in enumerate(analysis["top_performing_posts"], 1):
        print(f"\n{i}. Engagement Score: {post['engagement_score']}")
        print(f"   Content: {post['content']}")
        print(f"   Type: {post['content_type']}")
        print(f"   Metrics - Likes: {post['likes']}, Comments: {post['comments']}, Shares: {post['shares']}")

if __name__ == "__main__":
    analysis = analyze_training_data()
    print_analysis(analysis)
    export_analysis(analysis) 