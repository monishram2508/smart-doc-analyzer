import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent.parent
data_folder = project_root / "data"
chroma_db_folder = project_root / "chroma_db"

def ingest_documents():
    print("Starting Local Ingestion (Ollama)")

    print("🔌 Connecting to Ollama (nomic-embed-text)")
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    db_client = chromadb.PersistentClient(path=str(chroma_db_folder))
    chroma_collection = db_client.get_or_create_collection("legal_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("📂 Reading PDFs...")
    documents = SimpleDirectoryReader(str(data_folder)).load_data()

    print(f"📄 Found {len(documents)} pages. Embedding locally.")
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        show_progress=True
    )
    print("SUCCESS: Local Vectors stored.")

if __name__ == "__main__":
    ingest_documents()