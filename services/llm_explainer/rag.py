from sentence_transformers import SentenceTransformer
from supabase import create_client
import os
import asyncio

# Load embedding model once (important for performance)
_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    """
    Convert text → vector (384 floats)
    """
    vector = _embedder.encode(text)

    # numpy array → Python list
    return vector.tolist()


def _get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        return None

    return create_client(url, key)


async def search_similar_incidents(query: str, limit: int = 5) -> list[dict]:
    try:
        supabase = _get_supabase()
        if not supabase:
            return []

        # 1. Embed query
        query_vector = embed(query)

        # 2. Call RPC (run in thread to avoid blocking)
        def _rpc_call():
            return supabase.rpc(
                "match_incidents",
                {
                    "query_embedding": query_vector,
                    "match_threshold": 0.5,   # ← add this
                    "match_count": limit
                }
            ).execute()

        result = await asyncio.to_thread(_rpc_call)

        # 3. Return data
        return result.data if result.data else []

    except Exception:
        return []