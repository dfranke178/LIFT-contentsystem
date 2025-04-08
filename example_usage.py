from src.utils.feedback_loop import FeedbackLoop
import time
from typing import List

def main():
    # Initialize the feedback loop with LinkedIn credentials (optional)
    # Replace with your LinkedIn credentials if you want to use automatic collection
    feedback_loop = FeedbackLoop(
        linkedin_username=None,  # Your LinkedIn username
        linkedin_password=None   # Your LinkedIn password
    )

    # Example LinkedIn post URLs for automatic collection
    post_urls = [
        "https://www.linkedin.com/feed/update/activity-123",
        "https://www.linkedin.com/feed/update/activity-456"
    ]

    # Add some initial example feedback entries
    feedback_entries = [
        {
            "content_id": "article_123",
            "metrics": {
                "clarity": 0.85,
                "engagement": 0.65,
                "call_to_action": 0.90,
                "content_type": "article"
            },
            "comments": "Well-structured article with clear points. Could use more engaging elements."
        },
        {
            "content_id": "article_124",
            "metrics": {
                "clarity": 0.75,
                "engagement": 0.70,
                "call_to_action": 0.85,
                "content_type": "article"
            },
            "comments": "Good call to action, but needs better clarity in the middle section."
        },
        {
            "content_id": "media_101",
            "metrics": {
                "clarity": 0.90,
                "engagement": 0.95,
                "call_to_action": 0.80,
                "content_type": "media"
            },
            "comments": "Highly engaging visual content. Clear message and good engagement."
        }
    ]

    # Add example feedback entries
    for entry in feedback_entries:
        feedback_loop.add_feedback(
            content_id=entry["content_id"],
            metrics=entry["metrics"],
            comments=entry["comments"]
        )

    # Demonstrate automatic metric collection (requires LinkedIn credentials)
    print("\nAttempting automatic metric collection...")
    feedback_loop.collect_metrics_automatically(post_urls)

    # Demonstrate ML-based pattern analysis
    print("\nAnalyzing patterns with machine learning...")
    patterns = feedback_loop.analyze_patterns()
    print("\nML Patterns:")
    for pattern in patterns["patterns"]:
        print(f"- {pattern}")
    print("\nCluster Insights:")
    for cluster_id, insights in patterns["clusters"].items():
        print(f"\nCluster {cluster_id}:")
        print(f"Size: {insights['size']}")
        print(f"Average Metrics: {insights['avg_metrics']}")
        print(f"Top Performing Posts: {insights['top_posts']}")

    # Start scheduled analysis (runs every 24 hours)
    print("\nStarting scheduled analysis...")
    feedback_loop.schedule_analysis(interval_hours=24)

    # Let it run for a minute to demonstrate scheduling
    print("Waiting for initial analysis to complete...")
    time.sleep(60)

    # Stop the scheduler
    feedback_loop.stop_scheduler()
    print("\nDemo complete!")

if __name__ == "__main__":
    main() 