import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# --- ROBUST PATH SETUP (The Fix) ---
# 1. Get the absolute path of THIS script (ingest.py)
current_script_path = Path(__file__).resolve()

# 2. Find the Project Root (Go up 2 levels: src -> backend -> root)
project_root = current_script_path.parent.parent.parent

# 3. Define the path to the data folder and .env file securely
data_folder = project_root / "data"
env_file = project_root / ".env"
chroma_db_folder = project_root / "chroma_db"

print(f"Project Root detected at: {project_root}")
print(f"Looking for data in: {data_folder}")
# -----------------------------------

# Load .env from the specific path
load_dotenv(env_file)

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(f"API Key missing. Checked file: {env_file}")

def ingest_documents():
    print("Starting Ingestion Process...")

    # Ensure data folder exists
    if not data_folder.exists():
        raise ValueError(f"Error: The folder '{data_folder}' does not exist. Please create it and add a PDF.")

    Settings.embedding = OpenAIEmbedding(model="text-embedding-3-small")

    # Use the absolute path for the database too
    db_client = chromadb.PersistentClient(path=str(chroma_db_folder))
    chroma_collection = db_client.get_or_create_collection("legal_docs")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Reading PDFs.")
    # Use the robust 'data_folder' path we defined earlier
    documents = SimpleDirectoryReader(str(data_folder)).load_data()
    
    if not documents:
        print("No PDFs found! Please paste a PDF into the 'data' folder.")
        return

    print(f"Found {len(documents)} pages. Chunking and Embedding now...")

    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        show_progress=True
    )

    print(f"SUCCESS: Vectors stored in {chroma_db_folder}")

if __name__ == "__main__":
    ingest_documents()