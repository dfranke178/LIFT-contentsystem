from typing import Dict, List, Optional
import json
from pathlib import Path
import logging
from datetime import datetime, timedelta
import os
import schedule
import time
import threading
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
from linkedin_api import Linkedin
import requests

class FeedbackLoop:
    """Implements a continuous improvement feedback loop for content generation."""
    
    def __init__(self, linkedin_username: Optional[str] = None, linkedin_password: Optional[str] = None):
        self.feedback_dir = Path("feedback_data")
        self.feedback_path = self.feedback_dir / "feedback.json"
        self.improvements_path = self.feedback_dir / "improvements.json"
        self.model_path = self.feedback_dir / "ml_model.json"
        self._ensure_files()
        
        # Initialize LinkedIn API if credentials are provided
        self.linkedin_api = None
        if linkedin_username and linkedin_password:
            self.linkedin_api = Linkedin(linkedin_username, linkedin_password)
        
        # Initialize ML components
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        
        # Initialize scheduling
        self.scheduler_thread = None
        self.is_running = False

    def _ensure_files(self):
        """Ensure necessary directories and files exist."""
        try:
            os.makedirs(self.feedback_dir, exist_ok=True)
            
            # Initialize feedback file if it doesn't exist
            if not self.feedback_path.exists():
                with open(self.feedback_path, 'w') as f:
                    json.dump({"feedback": []}, f)
            
            # Initialize improvements file if it doesn't exist
            if not self.improvements_path.exists():
                with open(self.improvements_path, 'w') as f:
                    json.dump({"best_practices": {}, "ml_insights": []}, f)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize feedback system: {str(e)}")

    def collect_metrics_automatically(self, post_urls: List[str]) -> None:
        """Automatically collect metrics from LinkedIn posts."""
        if not self.linkedin_api:
            print("Warning: LinkedIn API not initialized. Please provide credentials.")
            return

        try:
            for url in post_urls:
                # Extract post ID from URL
                post_id = url.split('activity-')[-1]
                
                # Get post data from LinkedIn
                post_data = self.linkedin_api.get_post(post_id)
                
                if post_data:
                    metrics = {
                        "likes": post_data.get("numLikes", 0),
                        "comments": post_data.get("numComments", 0),
                        "shares": post_data.get("numShares", 0),
                        "views": post_data.get("views", 0)
                    }
                    
                    # Calculate normalized engagement scores
                    total_interactions = sum(metrics.values())
                    engagement_score = min(total_interactions / 1000, 1.0)  # Normalize to 0-1
                    
                    # Add feedback entry
                    self.add_feedback(
                        content_id=post_id,
                        metrics={
                            "engagement": engagement_score,
                            "content_type": post_data.get("type", "post"),
                            **metrics  # Include raw metrics
                        },
                        comments=f"Automatically collected metrics for post {post_id}"
                    )
                    
        except Exception as e:
            print(f"Warning: Error collecting metrics: {str(e)}")

    def analyze_patterns(self) -> Dict:
        """Analyze patterns using machine learning."""
        try:
            # Load feedback data
            with open(self.feedback_path, 'r') as f:
                data = json.load(f)
            
            if not data["feedback"]:
                return {"patterns": [], "clusters": {}}
            
            # Convert feedback to DataFrame
            df = pd.DataFrame([
                {
                    "content_id": entry["content_id"],
                    "engagement": entry["metrics"].get("engagement", 0),
                    "clarity": entry["metrics"].get("clarity", 0),
                    "call_to_action": entry["metrics"].get("call_to_action", 0)
                }
                for entry in data["feedback"]
            ])
            
            # Prepare features for clustering
            features = df[["engagement", "clarity", "call_to_action"]].values
            scaled_features = self.scaler.fit_transform(features)
            
            # Perform clustering
            clusters = self.kmeans.fit_predict(scaled_features)
            
            # Analyze patterns within clusters
            patterns = []
            cluster_insights = {}
            
            for cluster_id in range(self.kmeans.n_clusters):
                cluster_mask = clusters == cluster_id
                cluster_data = df[cluster_mask]
                
                if len(cluster_data) > 0:
                    avg_metrics = cluster_data.mean().to_dict()
                    cluster_insights[f"cluster_{cluster_id}"] = {
                        "size": len(cluster_data),
                        "avg_metrics": avg_metrics,
                        "top_posts": cluster_data.nlargest(3, "engagement")["content_id"].tolist()
                    }
                    
                    # Generate insights
                    if avg_metrics["engagement"] > 0.8:
                        patterns.append(f"High-performing cluster {cluster_id} found - analyze top posts for success factors")
            
            # Save ML insights
            with open(self.improvements_path, 'r+') as f:
                improvements_data = json.load(f)
                improvements_data["ml_insights"] = patterns
                f.seek(0)
                json.dump(improvements_data, f, indent=2)
            
            return {
                "patterns": patterns,
                "clusters": cluster_insights
            }
            
        except Exception as e:
            print(f"Warning: Error in pattern analysis: {str(e)}")
            return {"patterns": [], "clusters": {}}

    def schedule_analysis(self, interval_hours: int = 24):
        """Schedule periodic analysis runs."""
        def run_scheduled_analysis():
            print(f"\n[{datetime.now()}] Running scheduled analysis...")
            
            # Run automated collection (if URLs are configured)
            # self.collect_metrics_automatically(configured_urls)
            
            # Run pattern analysis
            patterns = self.analyze_patterns()
            
            # Run regular feedback analysis
            analysis = self.analyze_feedback()
            
            # Combine insights
            all_insights = {
                "timestamp": datetime.now().isoformat(),
                "metric_trends": analysis["metric_trends"],
                "recommendations": analysis["recommendations"],
                "ml_patterns": patterns["patterns"],
                "clusters": patterns["clusters"]
            }
            
            # Save insights to file
            report_path = self.feedback_dir / f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(report_path, 'w') as f:
                json.dump(all_insights, f, indent=2)
            
            print(f"Analysis complete. Report saved to {report_path}")

        def run_scheduler():
            schedule.every(interval_hours).hours.do(run_scheduled_analysis)
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)

        # Start the scheduler in a separate thread
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=run_scheduler)
        self.scheduler_thread.start()
        
        # Run initial analysis
        run_scheduled_analysis()
        
        print(f"Scheduled analysis every {interval_hours} hours")

    def stop_scheduler(self):
        """Stop the scheduled analysis."""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
            print("Scheduler stopped")

    def analyze_feedback(self) -> Dict:
        """Analyze feedback and return insights based on actual feedback data."""
        try:
            with open(self.feedback_path, 'r') as f:
                feedback_data = json.load(f)
            
            feedback = feedback_data["feedback"]
            if not feedback:
                return {
                    "metric_trends": {},
                    "recommendations": ["No feedback data available yet for analysis"]
                }
            
            # Calculate average metrics
            metrics_sum = {}
            metrics_count = {}
            
            for entry in feedback:
                for metric, value in entry["metrics"].items():
                    if isinstance(value, (int, float)):  # Only process numerical metrics
                        metrics_sum[metric] = metrics_sum.get(metric, 0) + value
                        metrics_count[metric] = metrics_count.get(metric, 0) + 1
            
            # Calculate averages and identify areas for improvement
            metric_trends = {}
            recommendations = []
            
            for metric in metrics_sum:
                avg_value = metrics_sum[metric] / metrics_count[metric]
                metric_trends[metric] = round(avg_value, 2)
                
                # Generate recommendations based on metric values
                if avg_value < 0.7:
                    recommendations.append(f"Focus on improving {metric} - currently below target")
                elif avg_value < 0.8:
                    recommendations.append(f"Consider enhancing {metric} for better performance")
            
            # Add general recommendations based on comments analysis
            comments_text = " ".join(entry["comments"] for entry in feedback)
            if "engaging" in comments_text.lower():
                recommendations.append("Multiple feedback entries mention engagement - consider adding more interactive elements")
            if "clarity" in comments_text.lower():
                recommendations.append("Pay attention to content clarity based on feedback patterns")
            
            return {
                "metric_trends": metric_trends,
                "recommendations": recommendations
            }
        except Exception as e:
            print(f"Warning: Could not analyze feedback: {str(e)}")
            return {"metric_trends": {}, "recommendations": []}
    
    def get_best_practices(self, area: Optional[str] = None) -> List[str]:
        """Get best practices, optionally filtered by area."""
        try:
            with open(self.improvements_path, 'r') as f:
                practices = json.load(f)
            
            if area and area in practices["best_practices"]:
                return practices["best_practices"][area]
            return [
                "Use clear and concise language",
                "Include a strong call-to-action",
                "Focus on value proposition"
            ]
        except Exception as e:
            print(f"Warning: Could not retrieve best practices: {str(e)}")
            return []
    
    def add_feedback(self, content_id: str, metrics: Dict, comments: str):
        """Add new feedback with timestamp."""
        try:
            with open(self.feedback_path, 'r') as f:
                data = json.load(f)
            
            feedback_entry = {
                "content_id": content_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "comments": comments
            }
            
            data["feedback"].append(feedback_entry)
            
            with open(self.feedback_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not add feedback: {str(e)}")
    
    def get_feedback_history(self, content_type: Optional[str] = None) -> List[Dict]:
        """Get feedback history, optionally filtered by content type."""
        try:
            with open(self.feedback_path, 'r') as f:
                data = json.load(f)
            
            feedback = data["feedback"]
            if content_type:
                feedback = [f for f in feedback if f.get("content_type") == content_type]
            
            return feedback
        except Exception as e:
            print(f"Warning: Could not retrieve feedback history: {str(e)}")
            return [] 