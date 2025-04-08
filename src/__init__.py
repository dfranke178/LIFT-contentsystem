from src.data_processor import DataProcessor
from src.utils import save_json, create_timestamp
from src.utils.feedback_loop import FeedbackLoop

# Use the DataProcessor
processor = DataProcessor()
processor.load_data("your_data.csv")
stats = processor.process_data()

# Use the utilities
timestamp = create_timestamp()
save_json(stats, f"results_{timestamp}.json")

# Initialize the FeedbackLoop
feedback_loop = FeedbackLoop(
    feedback_file="data/feedback.json",
    improvement_file="data/improvements.json"
)

analysis = feedback_loop.analyze_feedback(
    content_type="article",
    time_window_days=30
)

recommendations = analysis["recommendations"]