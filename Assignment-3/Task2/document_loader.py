from pathlib import Path


DOCUMENT_PATH = Path("data/edxso_faqs.txt")


def load_document(file_path: Path) -> str:
    """Load the FAQ document from a text file."""

    if not file_path.exists():
        raise FileNotFoundError(f"FAQ document not found: {file_path}")

    text = file_path.read_text(encoding="utf-8").strip()

    if not text:
        raise ValueError("FAQ document is empty.")

    return text


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 15) -> list[str]:
    """Split the document into overlapping word-based chunks."""

    if not text.strip():
        raise ValueError("Cannot create chunks from empty text.")

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


if __name__ == "__main__":
    try:
        document = load_document(DOCUMENT_PATH)
        chunks = chunk_text(document)

        print(f"Document loaded successfully.")
        print(f"Total chunks created: {len(chunks)}")

        print("\nFirst chunk:")
        print(chunks[0])

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")