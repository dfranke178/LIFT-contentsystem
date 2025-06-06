import json
from pathlib import Path
from typing import List

try:
    from sentence_transformers import SentenceTransformer, util
    _HAS_ST = True
except ImportError:
    _HAS_ST = False

MODEL_NAME = 'all-MiniLM-L6-v2'
POSTS_PATH = Path('data_store/authentic_posts.json')


def retrieve_relevant_posts(user_topic: str, top_k: int = 2, posts_path: Path = POSTS_PATH) -> List[str]:
    """
    Retrieve the most relevant authentic posts for a given topic using semantic similarity.
    Args:
        user_topic (str): The topic to match against posts.
        top_k (int): Number of top posts to return.
        posts_path (Path): Path to authentic_posts.json.
    Returns:
        List[str]: List of post contents.
    """
    if not _HAS_ST:
        raise ImportError("sentence-transformers is required for semantic retrieval. Please install it via pip.")
    with open(posts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    posts = data.get("authentic_posts", [])
    post_texts = [post["content"] for post in posts if post.get("content")]
    if not post_texts:
        return []
    model = SentenceTransformer(MODEL_NAME)
    topic_embedding = model.encode(user_topic, convert_to_tensor=True)
    post_embeddings = model.encode(post_texts, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(topic_embedding, post_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_k]
    return [post_texts[i] for i in top_indices] 