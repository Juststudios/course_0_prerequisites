"""vector_search.py - Pure-Python vector embeddings and Top-K cosine similarity retrieval for RAG.

Key concepts demonstrated:
1. Calculating Euclidean L2 norm and dot product.
2. Cosine similarity calculation between semantic vectors.
3. Unit-normalization of embeddings.
4. Top-K nearest neighbor document retrieval.
"""

from typing import List, Dict, Any, Tuple
import math
import heapq


def dot_product(u: List[float], v: List[float]) -> float:
    """Computes the scalar dot product of two vectors."""
    if len(u) != len(v):
        raise ValueError(f"Vector dimension mismatch: {len(u)} != {len(v)}")
    return sum(a * b for a, b in zip(u, v))


def euclidean_norm(v: List[float]) -> float:
    """Computes the L2 Euclidean norm of a vector."""
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(u: List[float], v: List[float]) -> float:
    """Computes the cosine of the angle between two vectors."""
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return dot_product(u, v) / (norm_u * norm_v)


def normalize_vector(v: List[float]) -> List[float]:
    """Scales a vector to unit length (L2 norm = 1.0)."""
    norm = euclidean_norm(v)
    if norm == 0.0:
        return v[:]
    return [x / norm for x in v]


class InMemoryVectorStore:
    """Simple semantic search engine for Retrieval-Augmented Generation (RAG)."""

    def __init__(self) -> None:
        self.documents: List[Dict[str, Any]] = []

    def add_document(self, doc_id: str, text: str, embedding: List[float]) -> None:
        """Adds a document with its pre-computed normalized embedding."""
        self.documents.append({
            "id": doc_id,
            "text": text,
            "embedding": normalize_vector(embedding)
        })

    def search(self, query_embedding: List[float], top_k: int = 2) -> List[Tuple[float, Dict[str, Any]]]:
        """Searches documents using cosine similarity and returns top_k results."""
        norm_query = normalize_vector(query_embedding)
        scored = []
        for doc in self.documents:
            # For unit-normalized vectors, cosine similarity is simply the dot product!
            score = dot_product(norm_query, doc["embedding"])
            scored.append((score, doc))

        # Return top_k sorted by descending score
        return heapq.nlargest(top_k, scored, key=lambda x: x[0])


def main() -> None:
    print("=== Module 15: Vector Embeddings & Cosine Search Demo ===")

    # 1. Test mathematical properties of cosine similarity
    v_a = [1.0, 0.0, 0.0]
    v_b = [1.0, 0.0, 0.0]
    v_c = [0.0, 1.0, 0.0]
    v_d = [-1.0, 0.0, 0.0]

    # Identical vectors -> similarity 1.0
    assert math.isclose(cosine_similarity(v_a, v_b), 1.0)
    # Orthogonal vectors -> similarity 0.0
    assert math.isclose(cosine_similarity(v_a, v_c), 0.0)
    # Opposite vectors -> similarity -1.0
    assert math.isclose(cosine_similarity(v_a, v_d), -1.0)
    print("[OK] Cosine similarity mathematical boundaries (1, 0, -1) verified.")

    # 2. Test unit normalization property
    raw_vec = [3.0, 4.0]
    norm_vec = normalize_vector(raw_vec)
    assert math.isclose(euclidean_norm(norm_vec), 1.0)
    assert math.isclose(norm_vec[0], 0.6) and math.isclose(norm_vec[1], 0.8)
    print("[OK] Vector normalization verified.")

    # 3. Test In-Memory Vector Store Top-K retrieval
    store = InMemoryVectorStore()
    # Simulated 4-D embedding space:
    # Dim 0: Python / coding
    # Dim 1: Async / event loop
    # Dim 2: Cooking / recipes
    # Dim 3: Astronomy / space
    store.add_document("doc_1", "Asyncio event loops in Python", [0.9, 0.8, 0.0, 0.0])
    store.add_document("doc_2", "How to bake sourdough bread", [0.0, 0.0, 0.95, 0.0])
    store.add_document("doc_3", "James Webb telescope images", [0.0, 0.0, 0.1, 0.9])
    store.add_document("doc_4", "Python callables and decorators", [0.85, 0.2, 0.0, 0.0])

    # Search for "Python asynchronous coroutines" -> high on dim 0 and dim 1
    query_vector = [0.8, 0.7, 0.0, 0.0]
    results = store.search(query_vector, top_k=2)

    assert len(results) == 2
    top_doc = results[0][1]
    top_score = results[0][0]
    second_doc = results[1][1]

    assert top_doc["id"] == "doc_1"
    assert second_doc["id"] == "doc_4"
    assert top_score > 0.95
    print(f"[OK] Top result: '{top_doc['text']}' with similarity score {top_score:.4f}")
    print(f"[OK] Second result: '{second_doc['text']}' with score {results[1][0]:.4f}")

    print("All tests in vector_search.py passed successfully!\n")


if __name__ == "__main__":
    main()
