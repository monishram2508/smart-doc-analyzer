# Smart Document Analyzer (RAG Pipeline)

A Retrieval-Augmented Generation (RAG) tool designed to help legal and medical professionals query complex PDF documents. Built with Python, LlamaIndex, and Streamlit, this application reduces document review time by extracting specific answers with citations.

## Tech Stack
- Language: Python 3.9.6
- AI Engine: LlamaIndex & OpenAI GPT-4
- Vector Database: ChromaDB
- Frontend: Streamlit

## Project Structure
- `/src/backend`: Core RAG logic and embedding generation.
- `/src/frontend`: Streamlit UI components.
- `/data`: Sample legal contracts and medical reports for testing.

## Key Features
- Accurate Retrieval: Uses semantic search to find relevant document chunks.
- Citation Support: Returns the specific page number for every answer.
- Hallucination Check: Engineered to strictly answer from the provided context.