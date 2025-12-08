# utils/document_processor.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_text(file_path, chunk_size=1000, chunk_overlap=100):
    """Chunk text file into smaller documents"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}")
        print("Make sure to create a .txt file in data/study_materials/")
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    print(f"✅ Split document into {len(documents)} chunks")
    return documents
