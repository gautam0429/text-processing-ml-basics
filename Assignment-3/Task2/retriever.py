from pathlib import Path

from sentence_transformers import SentenceTransformer

from document_loader import load_document, chunk_text
from embeddings import create_embeddings
from vector_store import build_vector_store


DOCUMENT_PATH = Path("data/edxso_faqs.txt")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3


def retrieve_chunks(
    query: str,
    model: SentenceTransformer,
    index,
    chunks: list[str],
    top_k: int = TOP_K
) -> list[str]:
    """Retrieve the most relevant document chunks for a query."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if not chunks:
        raise ValueError("No document chunks are available.")

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    k = min(top_k, len(chunks))

    scores, indices = index.search(query_embedding, k)

    results = []

    for score, index_value in zip(scores[0], indices[0]):
        if 0 <= index_value < len(chunks):
            results.append({
                "score": float(score),
                "text": chunks[index_value]
            })

    return results


if __name__ == "__main__":
    try:
        document = load_document(DOCUMENT_PATH)
        chunks = chunk_text(document)

        model = SentenceTransformer(MODEL_NAME)

        embeddings = create_embeddings(
            chunks,
            model
        )

        index = build_vector_store(embeddings)

        query = "How can I schedule a mentoring session?"

        results = retrieve_chunks(
            query,
            model,
            index,
            chunks,
            TOP_K
        )

        print(f"\nUser Query:")
        print(query)

        print(f"\nTop {len(results)} Relevant Chunks:")

        for position, result in enumerate(results, start=1):
            print(f"\nResult {position}")
            print(f"Similarity Score: {result['score']:.4f}")
            print(f"Text: {result['text']}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")