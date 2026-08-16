import faiss
import numpy as np

from pathlib import Path
from document_loader import load_document, chunk_text
from embeddings import create_embeddings
from sentence_transformers import SentenceTransformer


DOCUMENT_PATH = Path("data/edxso_faqs.txt")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store(embeddings: np.ndarray):
    """Create a FAISS index using cosine similarity."""

    if embeddings.size == 0:
        raise ValueError("Cannot create a vector store from empty embeddings.")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings.astype("float32"))

    return index


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

        print("FAISS vector store created successfully.")
        print(f"Number of vectors stored: {index.ntotal}")
        print(f"Vector dimensions: {index.d}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")