# utils/pdf_processor.py
import pdfplumber
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        return None

def chunk_pdf_text(pdf_path, chunk_size=1000, chunk_overlap=100):
    """Extract and chunk PDF text"""
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    print(f"✅ Split PDF into {len(documents)} chunks")
    return documents
