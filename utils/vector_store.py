# utils/vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings 
from config.settings import GROQ_API_KEY, GROQ_MODEL, VECTOR_DB_PATH
import os

# Use free local embeddings (no API cost!)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(documents):
    """Create FAISS vector store from documents"""
    vector_store = FAISS.from_documents(documents, embeddings)
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vector_store.save_local(VECTOR_DB_PATH)
    print(f"✅ Vector store created and saved to {VECTOR_DB_PATH}")
    return vector_store

def load_vector_store():
    """Load existing FAISS vector store"""
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(f"Vector store not found at {VECTOR_DB_PATH}")
    
    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"✅ Vector store loaded from {VECTOR_DB_PATH}")
    return vector_store

def search_vector_store(vector_store, query, k=3):
    """Search vector store for relevant documents"""
    results = vector_store.similarity_search(query, k=k)
    return results
