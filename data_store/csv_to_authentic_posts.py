import csv
import json
import os

CSV_PATH = "data_store/LinkedIn Posts-LIFT Training Data.csv"
JSON_PATH = "data_store/authentic_posts.json"

def parse_emojis(text):
    # Simple emoji extraction (can be improved)
    return [c for c in text if ord(c) > 10000]

def to_bool(val):
    if isinstance(val, str):
        return val.strip().lower() in ["yes", "true", "1"]
    return bool(val)

def main():
    posts = []
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Map spreadsheet columns to JSON fields
            post = {
                "post_id": row.get("POST_ID", "").strip(),
                "content": row.get("POST_TEXT", "").strip(),
                "metadata": {
                    "success_metrics": {
                        "likes": int(row.get("LIKES", "0").replace(",", "")),
                        "comments": int(row.get("COMMENTS", "0").replace(",", "")),
                        "shares": int(row.get("SHARES", "0").replace(",", "")),
                        "impressions": int(row.get("IMPRESSIONS", "0").replace(",", "")),
                        "engagement_rate": float(row.get("ENGAGEMENT_RATE", "0").replace(",", ""))
                    },
                    "voice_elements": {
                        "tone": row.get("TONE", "").strip(),
                        "style": row.get("VOICE_ELEMENTS", "").strip(),
                        "personal_touch": row.get("PERSONAL_TOUCH", "").strip(),
                        "professional_depth": row.get("WHY_SUCCESSFUL", "").strip(),
                        "unique_phrases": [],
                        "emotion_usage": row.get("EMOTION_USAGE", "").strip(),
                        "storytelling_elements": []
                    },
                    "content_type": row.get("CONTENT_TYPE", "").strip(),
                    "topic": row.get("TOPIC", "").strip(),
                    "why_successful": row.get("WHY_SUCCESSFUL", "").strip(),
                    "edits_made": [e.strip() for e in row.get("EDITS_MADE", "").split(";") if e.strip()],
                    "posting_date": row.get("DATE", "").strip(),
                    "target_audience": row.get("TARGET_AUDIENCE", "").strip(),
                    "key_message": row.get("KEY_MESSAGE", "").strip(),
                    "formatting_elements": {
                        "emojis_used": parse_emojis(row.get("POST_TEXT", "")),
                        "bullet_points": to_bool(row.get("BULLET_POINTS", "")),
                        "paragraph_breaks": row.get("PARAGRAPH_BREAKS", "").strip() or None,
                        "special_formatting": [f.strip() for f in row.get("FORMATTING_ELEMENTS", "").split(";") if f.strip()]
                    }
                }
            }
            posts.append(post)

    # Load or create voice_preferences (preserve if exists)
    voice_preferences = {}
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "voice_preferences" in data:
                    voice_preferences = data["voice_preferences"]
        except Exception:
            pass

    output = {
        "authentic_posts": posts,
        "voice_preferences": {
            "writing_style": {
                "sentence_structure": "Short, punchy sentences with rhetorical questions.",
                "paragraph_length": "1-2 sentences per paragraph.",
                "formatting_preferences": ["bullet points", "emojis"],
                "common_phrases": ["Here's the truth", "Let's dive in"],
                "typical_post_length": "150-250 words",
                "language_complexity": "Simple, direct, minimal jargon"
            },
            "tone_guidelines": {
                "professional_balance": "Informal, Professional but approachable",
                "personal_touch": "Share personal stories and lessons",
                "emotion_usage": "Motivational, positive",
                "humor_usage": "Occasional, light",
                "storytelling_approach": "Start with a hook, resolve with insight"
            },
            "content_structure": {
                "hook_preferences": "Bold statement or question",
                "body_structure": "Problem, solution, takeaway",
                "conclusion_style": "Call-to-action or reflection",
                "cta_preferences": ["Ask for comments", "Invite to connect"],
                "typical_sections": ["Hook", "Body", "Takeaway", "CTA"]
            },
            "engagement_patterns": {
                "best_performing_topics": ["Leadership", "Hiring", "Sales"],
                "best_performing_formats": ["Text-only", "Text with image"],
                "best_posting_times": ["Tuesday mornings", "Thursday afternoons"],
                "common_engagement_triggers": ["Personal stories", "Actionable tips"]
            }
        }
    }
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Converted {len(posts)} posts to {JSON_PATH}")

if __name__ == "__main__":
    main() 