# RAG Pipeline for Edxso Voice Agent

## Project Overview

This project implements the Retrieval-Augmented Generation (RAG) component of a voice-based AI assistant.

The pipeline takes a transcribed student query, searches an Edxso FAQ knowledge base for relevant information, and uses the retrieved content to build a grounded prompt for a language model.

The LLM response is mocked in this implementation so the complete RAG workflow can be demonstrated without requiring an external API key.

## Approach

The pipeline follows these steps:

1. Load the Edxso FAQ document.
2. Split the document into smaller overlapping chunks.
3. Generate embeddings for each chunk.
4. Store the embeddings in a FAISS vector index.
5. Convert the user's query into an embedding.
6. Retrieve the top-k relevant chunks using similarity search.
7. Build a prompt using the retrieved context and user query.
8. Pass the prompt to the response generation layer.
9. Return the final response.

## Architecture

Edxso FAQ Document
        ↓
Document Loading
        ↓
Text Chunking
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Store
        ↓
User Query
        ↓
Query Embedding
        ↓
Top-k Retrieval
        ↓
Relevant FAQ Context
        ↓
Prompt Construction
        ↓
LLM
        ↓
Final Response

## Technology Stack

- Python
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- NumPy
- Text-based FAQ knowledge base
- Mock LLM response layer

## Project Structure

Task2/
│
├── data/
│   └── edxso_faqs.txt
│
├── document_loader.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── prompt_builder.py
├── llm.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

## Component Overview

### document_loader.py

Loads the FAQ text file and splits the content into smaller overlapping chunks.

### embeddings.py

Uses `all-MiniLM-L6-v2` from Sentence Transformers to convert the text chunks into numerical embeddings.

### vector_store.py

Creates a FAISS index and stores the generated embeddings for similarity search.

### retriever.py

Converts the user's query into an embedding and retrieves the most relevant FAQ chunks from the FAISS index.

### prompt_builder.py

Combines the retrieved context with the user's query to create a grounded prompt for the LLM.

### llm.py

Contains the response generation layer. A mock response is used for the current implementation so no external API key is required.

### main.py

Connects all components and runs the complete RAG pipeline.

## Installation

Navigate to the Task2 directory:

    cd C:\Assignments\Assignment-3\Task2

Install the required dependencies:

    C:\Python314\python.exe -m pip install -r requirements.txt

The main dependencies are:

- sentence-transformers
- faiss-cpu
- numpy

## Running the Project

Run the complete pipeline with:

    C:\Python314\python.exe main.py

If Python is available in the system PATH, this can also be used:

    python main.py

## Example

### Input

    How can I schedule a mentoring session?

### Output

    User Query:
    How can I schedule a mentoring session?

    RAG Response:
    Mentoring sessions can be scheduled through the mentoring
    section of the Edxso platform, based on the available
    time slots shown there.

## How the RAG Pipeline Works

### 1. Document Loading and Chunking

The FAQ knowledge base is stored in:

    data/edxso_faqs.txt

The document is loaded and divided into smaller overlapping chunks. This makes it easier to retrieve only the information relevant to a particular student query.

During testing, the FAQ document produced 4 chunks.

### 2. Embedding Generation

Each chunk is converted into an embedding using:

    sentence-transformers/all-MiniLM-L6-v2

The model produces 384-dimensional embeddings.

The same model is used for the user's query so that the query and document chunks can be compared in the same vector space.

Test result:

    Number of embeddings: 4
    Embedding dimensions: 384

### 3. FAISS Vector Search

The generated embeddings are stored in a FAISS index.

FAISS is then used to find the chunks that are most similar to the user's query.

Test result:

    FAISS vector store created successfully.
    Number of vectors stored: 4
    Vector dimensions: 384

### 4. Retrieval

For each user query, the query is converted into an embedding and searched against the FAISS index.

The implementation retrieves the top 3 relevant chunks.

Example query:

    How can I schedule a mentoring session?

The highest-ranked result was related to mentoring session availability.

The highest similarity score during testing was:

    0.6906

### 5. Prompt Construction

The retrieved FAQ chunks are added to a prompt along with the user's question.

The prompt instructs the response generation layer to use the retrieved information and avoid making unsupported claims.

The basic structure is:

    Instructions
        +
    Retrieved FAQ Context
        +
    User Query
        ↓
       LLM
        ↓
    Response

### 6. Response Generation

The current implementation uses a mock LLM response.

This allows the complete RAG pipeline to be tested without an external API key.

The mock response layer can later be replaced with an actual LLM API or a local open-source model without changing the main retrieval components.

## Error Handling

Basic error handling is included for common cases such as:

- Missing FAQ document
- Empty FAQ document
- Empty user query
- Missing document chunks
- Empty embeddings
- Invalid vector store input
- Missing retrieved context
- Empty prompt

Errors are reported clearly instead of allowing invalid input to continue through the pipeline.

## Testing and Verification

The pipeline was tested locally step by step.

Document loading:

    Document loaded successfully.
    Total chunks created: 4

Embedding generation:

    Embeddings created successfully.
    Number of embeddings: 4
    Embedding dimensions: 384

FAISS vector store:

    FAISS vector store created successfully.
    Number of vectors stored: 4
    Vector dimensions: 384

Retrieval:

    Query:
    How can I schedule a mentoring session?

    Top similarity score:
    0.6906

Final pipeline test:

    User Query:
    How can I schedule a mentoring session?

    RAG Response:
    Mentoring sessions can be scheduled through the mentoring
    section of the Edxso platform, based on the available
    time slots shown there.

## Connection with the Voice Agent

In the complete voice assistant, this RAG pipeline would sit between ASR and the response generation/TTS components.

The overall flow would be:

Student Speech
      ↓
ASR
      ↓
Transcribed Query
      ↓
RAG Pipeline
      ↓
Relevant Knowledge
      ↓
LLM Response
      ↓
TTS
      ↓
Spoken Response

This allows the voice agent to use information from the Edxso knowledge base when answering student questions.

## Future Improvements

For a production implementation, the following improvements could be considered:

- Replace the mock LLM with an actual model.
- Persist the FAISS index instead of rebuilding it for every request.
- Improve chunking using document or FAQ boundaries.
- Store metadata with each chunk.
- Add a retrieval relevance threshold.
- Add source references to generated responses.
- Add conversation history for multi-turn interactions.
- Connect the RAG pipeline directly with ASR and TTS services.

## Conclusion

This project demonstrates a complete RAG workflow for the Edxso Voice Agent.

The system loads and chunks the FAQ knowledge base, generates embeddings using Sentence Transformers, stores them in FAISS, retrieves relevant information for a user query, and builds a grounded prompt for response generation.

The components are separated into individual modules so that the system can be extended later with a production LLM, persistent vector storage, and the ASR/TTS components of the complete voice agent.