from pathlib import Path

from sentence_transformers import SentenceTransformer

from document_loader import load_document, chunk_text
from embeddings import create_embeddings
from vector_store import build_vector_store
from retriever import retrieve_chunks


DOCUMENT_PATH = Path("data/edxso_faqs.txt")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3


def build_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    """Build a grounded prompt using the retrieved FAQ chunks."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if not retrieved_chunks:
        raise ValueError("No relevant context was retrieved.")

    context = "\n\n".join(
        result["text"] for result in retrieved_chunks
    )

    prompt = f"""You are an educational support assistant for Edxso.

Answer the user's question using only the information provided
in the context below.

If the answer cannot be found in the context, say that you
do not have enough information to answer the question.

Context:
{context}

Question:
{query}

Answer:"""

    return prompt


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

        prompt = build_prompt(
            query,
            results
        )

        print("\nGenerated LLM Prompt:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")