from pathlib import Path

from sentence_transformers import SentenceTransformer

from document_loader import load_document, chunk_text


DOCUMENT_PATH = Path("data/edxso_faqs.txt")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def create_embeddings(chunks: list[str], model: SentenceTransformer):
    """Convert text chunks into numerical embeddings."""

    if not chunks:
        raise ValueError("No text chunks were provided.")

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":
    try:
        document = load_document(DOCUMENT_PATH)
        chunks = chunk_text(document)

        print(f"Loaded {len(chunks)} text chunks.")

        print("Loading embedding model...")
        model = SentenceTransformer(MODEL_NAME)

        embeddings = create_embeddings(chunks, model)

        print("Embeddings created successfully.")
        print(f"Number of embeddings: {len(embeddings)}")
        print(f"Embedding dimensions: {embeddings.shape[1]}")

        print("\nFirst embedding:")
        print(embeddings[0][:10])

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")