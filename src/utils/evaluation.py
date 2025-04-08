from typing import Dict, List, Optional
import json
from pathlib import Path
import logging
from datetime import datetime
import nltk
import spacy
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class ContentEvaluator:
    """Evaluates content quality and maintains feedback for improvement."""
    
    def __init__(self, feedback_file: str = "data/feedback.json"):
        self.feedback_file = feedback_file
        self.logger = logging.getLogger(__name__)
        
        # Initialize NLP components
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self._ensure_feedback_file()
    
    def _ensure_feedback_file(self):
        """Ensure feedback file exists with proper structure."""
        feedback_path = Path(self.feedback_file)
        if not feedback_path.exists():
            feedback_path.parent.mkdir(parents=True, exist_ok=True)
            with open(feedback_path, 'w') as f:
                json.dump({
                    "feedback_history": [],
                    "content_examples": [],
                    "metrics_history": []
                }, f, indent=2)
    
    def evaluate_content(self, content: str, content_type: str, 
                        engagement_data: Optional[Dict] = None) -> Dict:
        """
        Evaluate content quality using NLP-based metrics.
        """
        doc = self.nlp(content)
        
        metrics = {
            "clarity": self._evaluate_clarity(doc),
            "engagement_potential": self._evaluate_engagement_potential(doc),
            "professional_tone": self._evaluate_professional_tone(doc),
            "value_proposition": self._evaluate_value_proposition(doc),
            "call_to_action": self._evaluate_call_to_action(doc),
            "content_type_specific": self._evaluate_content_type_specific(doc, content_type)
        }
        
        if engagement_data:
            metrics["engagement_accuracy"] = self._compare_engagement(
                metrics["engagement_potential"],
                engagement_data
            )
        
        self._store_metrics(metrics, content_type)
        return metrics
    
    def _evaluate_clarity(self, doc) -> float:
        """Evaluate content clarity using multiple readability metrics."""
        text = doc.text
        
        # Calculate various readability scores
        flesch_score = textstat.flesch_reading_ease(text)
        fog_score = textstat.gunning_fog(text)
        smog_score = textstat.smog_index(text)
        
        # Normalize scores to 0-1 range
        # Flesch score is inverted (higher is better)
        flesch_normalized = min(max((flesch_score - 30) / 70, 0), 1)
        # Fog and SMOG scores are direct (lower is better)
        fog_normalized = min(max(1 - (fog_score / 20), 0), 1)
        smog_normalized = min(max(1 - (smog_score / 15), 0), 1)
        
        # Calculate sentence length variation
        sentences = sent_tokenize(text)
        if len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            length_variation = 1 - (np.std(lengths) / np.mean(lengths))
        else:
            length_variation = 0.5
        
        # Combine scores with weights
        clarity_score = (
            0.4 * flesch_normalized +
            0.3 * fog_normalized +
            0.2 * smog_normalized +
            0.1 * length_variation
        )
        
        return round(clarity_score, 2)
    
    def _evaluate_engagement_potential(self, doc) -> float:
        """Evaluate potential engagement using linguistic features."""
        engagement_score = 0.0
        features = {
            'questions': 0,
            'emotional_words': 0,
            'personal_pronouns': 0,
            'action_verbs': 0
        }
        
        # Define engagement-related word lists
        emotional_words = {'amazing', 'excited', 'thrilled', 'incredible', 'wonderful',
                          'important', 'crucial', 'essential', 'valuable', 'beneficial'}
        action_verbs = {'learn', 'discover', 'explore', 'achieve', 'transform',
                       'improve', 'enhance', 'develop', 'create', 'build'}
        
        for token in doc:
            # Count questions
            if token.text.endswith('?'):
                features['questions'] += 1
            
            # Count emotional words
            if token.text.lower() in emotional_words:
                features['emotional_words'] += 1
            
            # Count personal pronouns
            if token.pos_ == 'PRON' and token.text.lower() in {'i', 'you', 'we', 'us'}:
                features['personal_pronouns'] += 1
            
            # Count action verbs
            if token.pos_ == 'VERB' and token.text.lower() in action_verbs:
                features['action_verbs'] += 1
        
        # Calculate engagement score based on features
        total_words = len(doc)
        if total_words > 0:
            engagement_score = (
                0.3 * min(features['questions'] / 2, 1) +  # Cap at 2 questions
                0.2 * min(features['emotional_words'] / 5, 1) +  # Cap at 5 emotional words
                0.2 * min(features['personal_pronouns'] / 3, 1) +  # Cap at 3 pronouns
                0.3 * min(features['action_verbs'] / 3, 1)  # Cap at 3 action verbs
            )
        
        return round(min(engagement_score, 1), 2)
    
    def _evaluate_professional_tone(self, doc) -> float:
        """Evaluate professional tone using linguistic analysis."""
        tone_score = 0.0
        features = {
            'formal_words': 0,
            'jargon_words': 0,
            'casual_words': 0,
            'sentence_structure': 0
        }
        
        # Define word lists for tone analysis
        formal_words = {'utilize', 'implement', 'facilitate', 'optimize', 'leverage',
                       'strategize', 'methodology', 'paradigm', 'synergy', 'initiative'}
        casual_words = {'hey', 'guys', 'awesome', 'cool', 'stuff', 'thing',
                       'kinda', 'sorta', 'gonna', 'wanna'}
        
        for token in doc:
            # Count formal words
            if token.text.lower() in formal_words:
                features['formal_words'] += 1
            
            # Count casual words
            if token.text.lower() in casual_words:
                features['casual_words'] += 1
        
        # Analyze sentence structure
        sentences = list(doc.sents)
        if sentences:
            avg_sentence_length = sum(len(sent) for sent in sentences) / len(sentences)
            features['sentence_structure'] = min(avg_sentence_length / 20, 1)  # Cap at 20 words
        
        # Calculate tone score
        total_words = len(doc)
        if total_words > 0:
            tone_score = (
                0.4 * min(features['formal_words'] / 5, 1) +  # Cap at 5 formal words
                0.3 * (1 - min(features['casual_words'] / 3, 1)) +  # Penalize casual words
                0.3 * features['sentence_structure']
            )
        
        return round(min(tone_score, 1), 2)
    
    def _evaluate_value_proposition(self, doc) -> float:
        """Evaluate clarity of value proposition."""
        value_score = 0.0
        features = {
            'benefit_phrases': 0,
            'problem_solution': 0,
            'unique_indicators': 0
        }
        
        # Define patterns for value proposition analysis
        benefit_indicators = {'benefit', 'advantage', 'value', 'improve', 'enhance',
                            'increase', 'reduce', 'save', 'optimize', 'streamline'}
        problem_indicators = {'challenge', 'problem', 'issue', 'pain', 'difficulty',
                            'struggle', 'obstacle', 'barrier', 'hurdle'}
        unique_indicators = {'unique', 'exclusive', 'only', 'first', 'innovative',
                           'revolutionary', 'groundbreaking', 'cutting-edge'}
        
        # Analyze sentences for value proposition components
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Check for benefit statements
            if any(word in sent_text for word in benefit_indicators):
                features['benefit_phrases'] += 1
            
            # Check for problem-solution structure
            if (any(word in sent_text for word in problem_indicators) and
                any(word in sent_text for word in benefit_indicators)):
                features['problem_solution'] += 1
            
            # Check for unique value indicators
            if any(word in sent_text for word in unique_indicators):
                features['unique_indicators'] += 1
        
        # Calculate value proposition score
        total_sentences = len(list(doc.sents))
        if total_sentences > 0:
            value_score = (
                0.4 * min(features['benefit_phrases'] / 2, 1) +  # Cap at 2 benefit phrases
                0.4 * min(features['problem_solution'] / 1, 1) +  # Cap at 1 problem-solution
                0.2 * min(features['unique_indicators'] / 2, 1)  # Cap at 2 unique indicators
            )
        
        return round(min(value_score, 1), 2)
    
    def _evaluate_call_to_action(self, doc) -> float:
        """Evaluate call-to-action effectiveness."""
        cta_score = 0.0
        features = {
            'action_verbs': 0,
            'urgency_indicators': 0,
            'clear_direction': 0
        }
        
        # Define CTA-related word lists
        action_verbs = {'join', 'register', 'sign', 'download', 'subscribe',
                       'learn', 'discover', 'explore', 'start', 'try'}
        urgency_indicators = {'now', 'today', 'limited', 'exclusive', 'special',
                            'offer', 'deadline', 'time', 'chance', 'opportunity'}
        
        # Analyze sentences for CTA components
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Check for action verbs
            if any(word in sent_text for word in action_verbs):
                features['action_verbs'] += 1
            
            # Check for urgency indicators
            if any(word in sent_text for word in urgency_indicators):
                features['urgency_indicators'] += 1
            
            # Check for clear direction (imperative sentences)
            if sent[0].pos_ == 'VERB' and sent[0].tag_ == 'VB':
                features['clear_direction'] += 1
        
        # Calculate CTA score
        total_sentences = len(list(doc.sents))
        if total_sentences > 0:
            cta_score = (
                0.4 * min(features['action_verbs'] / 2, 1) +  # Cap at 2 action verbs
                0.3 * min(features['urgency_indicators'] / 2, 1) +  # Cap at 2 urgency indicators
                0.3 * min(features['clear_direction'] / 1, 1)  # Cap at 1 clear direction
            )
        
        return round(min(cta_score, 1), 2)
    
    def _evaluate_content_type_specific(self, doc, content_type: str) -> Dict:
        """Evaluate content-type specific metrics."""
        metrics = {}
        
        if content_type == "media":
            # Analyze media post specific features
            metrics["visual_description_quality"] = self._evaluate_visual_description(doc)
            metrics["media_relevance"] = self._evaluate_media_relevance(doc)
        
        elif content_type == "article":
            # Analyze article specific features
            metrics["depth_of_insight"] = self._evaluate_depth_of_insight(doc)
            metrics["structure_quality"] = self._evaluate_structure_quality(doc)
        
        return metrics
    
    def _evaluate_visual_description(self, doc) -> float:
        """Evaluate quality of visual descriptions in media posts."""
        score = 0.0
        features = {
            'descriptive_adjectives': 0,
            'spatial_indicators': 0,
            'visual_verbs': 0
        }
        
        # Define visual description related words
        descriptive_adjs = {'clear', 'vibrant', 'detailed', 'sharp', 'colorful',
                          'striking', 'captivating', 'engaging', 'dynamic', 'vivid'}
        spatial_indicators = {'above', 'below', 'left', 'right', 'center',
                            'foreground', 'background', 'top', 'bottom', 'middle'}
        visual_verbs = {'show', 'display', 'depict', 'illustrate', 'present',
                       'highlight', 'feature', 'demonstrate', 'reveal', 'portray'}
        
        for token in doc:
            if token.text.lower() in descriptive_adjs:
                features['descriptive_adjectives'] += 1
            elif token.text.lower() in spatial_indicators:
                features['spatial_indicators'] += 1
            elif token.text.lower() in visual_verbs:
                features['visual_verbs'] += 1
        
        total_words = len(doc)
        if total_words > 0:
            score = (
                0.4 * min(features['descriptive_adjectives'] / 3, 1) +
                0.3 * min(features['spatial_indicators'] / 2, 1) +
                0.3 * min(features['visual_verbs'] / 2, 1)
            )
        
        return round(min(score, 1), 2)
    
    def _evaluate_media_relevance(self, doc) -> float:
        """Evaluate relevance of media content to the text."""
        score = 0.0
        features = {
            'media_references': 0,
            'contextual_links': 0
        }
        
        # Define media reference indicators
        media_refs = {'image', 'photo', 'picture', 'video', 'graphic',
                     'infographic', 'visual', 'illustration', 'diagram', 'chart'}
        
        for token in doc:
            if token.text.lower() in media_refs:
                features['media_references'] += 1
        
        # Check for contextual links between text and media
        sentences = list(doc.sents)
        if len(sentences) > 1:
            # Simple check for contextual flow
            features['contextual_links'] = min(len(sentences) / 5, 1)
        
        score = (
            0.6 * min(features['media_references'] / 2, 1) +
            0.4 * features['contextual_links']
        )
        
        return round(min(score, 1), 2)
    
    def _evaluate_depth_of_insight(self, doc) -> float:
        """Evaluate depth of insight in articles."""
        score = 0.0
        features = {
            'expert_terms': 0,
            'data_references': 0,
            'analysis_indicators': 0
        }
        
        # Define depth indicators
        expert_terms = {'research', 'study', 'analysis', 'findings', 'data',
                       'statistics', 'trend', 'pattern', 'correlation', 'impact'}
        analysis_indicators = {'because', 'therefore', 'thus', 'consequently',
                             'however', 'although', 'while', 'whereas', 'despite'}
        
        for token in doc:
            if token.text.lower() in expert_terms:
                features['expert_terms'] += 1
            elif token.text.lower() in analysis_indicators:
                features['analysis_indicators'] += 1
        
        # Check for data references
        for ent in doc.ents:
            if ent.label_ in ['CARDINAL', 'PERCENT', 'QUANTITY']:
                features['data_references'] += 1
        
        total_words = len(doc)
        if total_words > 0:
            score = (
                0.4 * min(features['expert_terms'] / 5, 1) +
                0.3 * min(features['data_references'] / 3, 1) +
                0.3 * min(features['analysis_indicators'] / 3, 1)
            )
        
        return round(min(score, 1), 2)
    
    def _evaluate_structure_quality(self, doc) -> float:
        """Evaluate structure quality of articles."""
        score = 0.0
        features = {
            'heading_structure': 0,
            'paragraph_length': 0,
            'transition_words': 0
        }
        
        # Define structure indicators
        transition_words = {'first', 'second', 'finally', 'moreover', 'furthermore',
                          'additionally', 'however', 'nevertheless', 'consequently',
                          'therefore', 'thus', 'hence', 'accordingly'}
        
        # Analyze document structure
        sentences = list(doc.sents)
        paragraphs = doc.text.split('\n\n')
        
        # Check paragraph length variation
        if len(paragraphs) > 1:
            para_lengths = [len(p.split()) for p in paragraphs]
            features['paragraph_length'] = 1 - (np.std(para_lengths) / np.mean(para_lengths))
        
        # Count transition words
        for token in doc:
            if token.text.lower() in transition_words:
                features['transition_words'] += 1
        
        # Calculate structure score
        total_words = len(doc)
        if total_words > 0:
            score = (
                0.4 * features['paragraph_length'] +
                0.3 * min(features['transition_words'] / 5, 1) +
                0.3 * min(len(paragraphs) / 5, 1)  # Reward having multiple paragraphs
            )
        
        return round(min(score, 1), 2)
    
    def _compare_engagement(self, predicted: float, actual: Dict) -> float:
        """Compare predicted engagement with actual engagement data."""
        # Normalize actual engagement metrics
        max_engagement = max(actual.values())
        if max_engagement == 0:
            return 0.0
        
        normalized_actual = {
            k: v / max_engagement for k, v in actual.items()
        }
        
        # Calculate average normalized actual engagement
        avg_actual = sum(normalized_actual.values()) / len(normalized_actual)
        
        # Calculate accuracy as 1 - absolute difference
        accuracy = 1 - abs(predicted - avg_actual)
        
        return round(max(0, min(accuracy, 1)), 2)
    
    def add_feedback(self, content: str, content_type: str, 
                    feedback: Dict, metrics: Dict) -> None:
        """
        Add feedback to the feedback history.
        
        Args:
            content (str): The content being evaluated
            content_type (str): Type of content
            feedback (Dict): User or system feedback
            metrics (Dict): Evaluation metrics
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "content_type": content_type,
            "feedback": feedback,
            "metrics": metrics
        }
        
        with open(self.feedback_file, 'r+') as f:
            data = json.load(f)
            data["feedback_history"].append(feedback_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    
    def _store_metrics(self, metrics: Dict, content_type: str) -> None:
        """Store metrics in the metrics history."""
        metrics_entry = {
            "timestamp": datetime.now().isoformat(),
            "content_type": content_type,
            "metrics": metrics
        }
        
        with open(self.feedback_file, 'r+') as f:
            data = json.load(f)
            data["metrics_history"].append(metrics_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    
    def get_feedback_history(self, content_type: Optional[str] = None) -> List[Dict]:
        """Retrieve feedback history, optionally filtered by content type."""
        with open(self.feedback_file, 'r') as f:
            data = json.load(f)
            if content_type:
                return [entry for entry in data["feedback_history"] 
                       if entry["content_type"] == content_type]
            return data["feedback_history"]
    
    def get_metrics_history(self, content_type: Optional[str] = None) -> List[Dict]:
        """Retrieve metrics history, optionally filtered by content type."""
        with open(self.feedback_file, 'r') as f:
            data = json.load(f)
            if content_type:
                return [entry for entry in data["metrics_history"] 
                       if entry["content_type"] == content_type]
            return data["metrics_history"] 