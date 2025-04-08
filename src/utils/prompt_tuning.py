from typing import Dict, List, Optional
import json
from pathlib import Path
import logging
from datetime import datetime
from .evaluation import ContentEvaluator

class PromptTuner:
    """Implements prompt-based fine-tuning using few-shot learning and adaptive prompting."""
    
    def __init__(self, examples_file: str = "data/content_examples.json"):
        self.examples_file = examples_file
        self.evaluator = ContentEvaluator()
        self.logger = logging.getLogger(__name__)
        self._ensure_examples_file()
    
    def _ensure_examples_file(self):
        """Ensure examples file exists with proper structure."""
        examples_path = Path(self.examples_file)
        if not examples_path.exists():
            examples_path.parent.mkdir(parents=True, exist_ok=True)
            with open(examples_path, 'w') as f:
                json.dump({
                    "examples": [],
                    "prompt_templates": {},
                    "adaptation_history": []
                }, f, indent=2)
    
    def add_example(self, content: str, content_type: str, 
                   metrics: Dict, context: Dict) -> None:
        """
        Add a new example to the content library.
        
        Args:
            content (str): The example content
            content_type (str): Type of content
            metrics (Dict): Evaluation metrics
            context (Dict): Context for the example
        """
        example = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "content_type": content_type,
            "metrics": metrics,
            "context": context
        }
        
        with open(self.examples_file, 'r+') as f:
            data = json.load(f)
            data["examples"].append(example)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    
    def get_few_shot_examples(self, content_type: str, 
                            metric_threshold: float = 0.8) -> List[Dict]:
        """
        Retrieve high-quality examples for few-shot learning.
        
        Args:
            content_type (str): Type of content
            metric_threshold (float): Minimum metric score for examples
            
        Returns:
            List[Dict]: Selected examples
        """
        with open(self.examples_file, 'r') as f:
            data = json.load(f)
            
        # Filter examples by content type and metric threshold
        examples = [
            ex for ex in data["examples"]
            if ex["content_type"] == content_type and
            all(score >= metric_threshold for score in ex["metrics"].values())
        ]
        
        # Sort by timestamp (most recent first)
        examples.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return examples[:5]  # Return top 5 examples
    
    def adapt_prompt(self, base_prompt: str, content_type: str,
                    feedback: Optional[Dict] = None) -> str:
        """
        Adapt prompt based on feedback and examples.
        
        Args:
            base_prompt (str): Original prompt template
            content_type (str): Type of content
            feedback (Optional[Dict]): Recent feedback
            
        Returns:
            str: Adapted prompt
        """
        # Get high-quality examples
        examples = self.get_few_shot_examples(content_type)
        
        # Start with the base prompt
        adapted_prompt = base_prompt
        
        # Add examples if available
        if examples:
            adapted_prompt += "\n\nHere are some successful examples:\n"
            for i, example in enumerate(examples, 1):
                adapted_prompt += f"\nExample {i}:\n"
                adapted_prompt += f"Context: {json.dumps(example['context'])}\n"
                adapted_prompt += f"Content: {example['content']}\n"
                adapted_prompt += f"Metrics: {json.dumps(example['metrics'])}\n"
        
        # Incorporate feedback if available
        if feedback:
            adapted_prompt += "\n\nRecent feedback and improvements:\n"
            for key, value in feedback.items():
                adapted_prompt += f"- {key}: {value}\n"
        
        # Store adaptation history
        self._store_adaptation(base_prompt, adapted_prompt, content_type)
        
        return adapted_prompt
    
    def _store_adaptation(self, original: str, adapted: str, 
                         content_type: str) -> None:
        """Store prompt adaptation history."""
        adaptation = {
            "timestamp": datetime.now().isoformat(),
            "content_type": content_type,
            "original_prompt": original,
            "adapted_prompt": adapted
        }
        
        with open(self.examples_file, 'r+') as f:
            data = json.load(f)
            data["adaptation_history"].append(adaptation)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    
    def get_adaptation_history(self, content_type: Optional[str] = None) -> List[Dict]:
        """Retrieve adaptation history, optionally filtered by content type."""
        with open(self.examples_file, 'r') as f:
            data = json.load(f)
            if content_type:
                return [entry for entry in data["adaptation_history"] 
                       if entry["content_type"] == content_type]
            return data["adaptation_history"]
    
    def update_prompt_templates(self, content_type: str, 
                              templates: Dict[str, str]) -> None:
        """
        Update prompt templates for a content type.
        
        Args:
            content_type (str): Type of content
            templates (Dict[str, str]): New prompt templates
        """
        with open(self.examples_file, 'r+') as f:
            data = json.load(f)
            if "prompt_templates" not in data:
                data["prompt_templates"] = {}
            data["prompt_templates"][content_type] = templates
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    
    def get_prompt_templates(self, content_type: str) -> Dict[str, str]:
        """Retrieve prompt templates for a content type."""
        with open(self.examples_file, 'r') as f:
            data = json.load(f)
            return data.get("prompt_templates", {}).get(content_type, {}) 