import os
from dotenv import load_dotenv

try:
    from llama_index.core import VectorStoreIndex, StorageContext
    from llama_index.vector_stores.chroma import ChromaVectorStore
    import chromadb
    REAL_AI_AVAILABLE = True
except Exception:
    REAL_AI_AVAILABLE = False

load_dotenv()

def get_query_engine():
    """
    This function returns a 'Query Engine'.
    If we have an API Key, it returns the real AI.
    If NOT, it returns a 'Mock' engine for testing.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or not REAL_AI_AVAILABLE:
        print("WARNING: No API Key found. Using MOCK mode.")
        return MockEngine()
        
    print("API Key found. connecting to Real AI.")
    
    # Real Logic (We will uncomment this later when payment works)
    # db_client = chromadb.PersistentClient(path="./chroma_db")
    # chroma_collection = db_client.get_or_create_collection("legal_docs")
    # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # index = VectorStoreIndex.from_vector_store(
    #     vector_store,
    #     embed_model=OpenAIEmbedding()
    # )
    # return index.as_query_engine()
    
    return MockEngine()

class MockEngine:
    """
    A fake AI that just repeats what you said.
    Used for testing the UI without spending money.
    """
    def query(self, question):
        return MockResponse(f"MOCK ANSWER: You asked '{question}'. \n\n(This is a placeholder. The UI works, but the AI is disconnected.)")

class MockResponse:
    def __init__(self, text):
        self.response = text
    
    def __str__(self):
        return self.response