from pathlib import Path

from sentence_transformers import SentenceTransformer

from document_loader import load_document, chunk_text
from embeddings import create_embeddings
from vector_store import build_vector_store
from retriever import retrieve_chunks
from prompt_builder import build_prompt
from llm import generate_response


DOCUMENT_PATH = Path("data/edxso_faqs.txt")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3


def run_rag_pipeline(query: str) -> str:
    """Run the complete RAG pipeline for a user query."""

    if not query.strip():
        raise ValueError("User query cannot be empty.")

    # Load and chunk the knowledge base
    document = load_document(DOCUMENT_PATH)
    chunks = chunk_text(document)

    # Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Create embeddings and build FAISS index
    embeddings = create_embeddings(chunks, model)
    index = build_vector_store(embeddings)

    # Retrieve relevant information
    retrieved_chunks = retrieve_chunks(
        query,
        model,
        index,
        chunks,
        TOP_K
    )

    # Build grounded LLM prompt
    prompt = build_prompt(
        query,
        retrieved_chunks
    )

    # Generate response
    response = generate_response(prompt)

    return response


if __name__ == "__main__":
    try:
        user_query = "How can I schedule a mentoring session?"

        print("User Query:")
        print(user_query)

        response = run_rag_pipeline(user_query)

        print("\nRAG Response:")
        print(response)

    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")