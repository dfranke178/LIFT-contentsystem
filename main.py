from src.utils.feedback_loop import FeedbackLoop
import json
from pathlib import Path

def setup_data_directories():
    """Create necessary directories and initial data files"""
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    
    # Create initial feedback file if it doesn't exist
    feedback_file = Path("data/feedback.json")
    if not feedback_file.exists():
        with open(feedback_file, "w") as f:
            json.dump({
                "article": [],
                "media": []
            }, f, indent=2)

def main():
    # Setup directories and initial files
    setup_data_directories()
    
    # 1. Initialize the feedback loop
    feedback_loop = FeedbackLoop(
        feedback_file="data/feedback.json",
        improvement_file="data/improvements.json"
    )
    
    # 2. Analyze feedback for a specific content type
    analysis = feedback_loop.analyze_feedback(
        content_type="article",
        time_window_days=30
    )
    
    # 3. Get recommendations
    recommendations = analysis["recommendations"]
    print("\nRecommendations:")
    for area, recs in recommendations.items():
        print(f"\n{area.upper()}:")
        for rec in recs:
            print(f"- {rec}")
    
    # 4. Access best practices
    best_practices = feedback_loop.get_best_practices()
    print("\nBest Practices:")
    for area, practices in best_practices.items():
        print(f"\n{area.upper()}:")
        for practice in practices:
            print(f"- {practice}")

if __name__ == "__main__":
    main() 