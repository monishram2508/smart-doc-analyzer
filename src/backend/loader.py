import sys
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
import chromadb

current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent.parent
chroma_db_folder = project_root / "chroma_db"

def get_query_engine():
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(model="llama3.2", request_timeout=300.0)

    db_client = chromadb.PersistentClient(path=str(chroma_db_folder))
    chroma_collection = db_client.get_or_create_collection("legal_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store,
    )
    return index.as_query_engine()