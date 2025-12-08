# agents/concept_explainer.py
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config.settings import GROQ_API_KEY, GROQ_MODEL
from utils.vector_store import search_vector_store

class ConceptExplainerAgent:
    def __init__(self, vector_store=None):
        """Initialize the concept explainer agent with Groq LLM"""
        self.llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.7,
            groq_api_key=GROQ_API_KEY
        )
        self.vector_store = vector_store
        self.chat_history = []
        
    def explain_concept(self, question):
        """Explain a concept using RAG (Retrieval Augmented Generation)"""
        if not self.vector_store:
            return "❌ No study materials loaded. Please upload documents first."
        
        # Step 1: Retrieve relevant context from vector store
        print(f"🔍 Searching for relevant information...")
        results = search_vector_store(self.vector_store, question, k=3)
        context = "\n\n".join([doc.page_content for doc in results])
        
        # Step 2: Create prompt with context
        prompt = f"""You are a helpful study assistant. Use the following context from study materials to answer the question.

Context from study materials:
{context}

Question: {question}

Instructions:
- Provide a clear, detailed explanation based on the context above
- Use examples from the context when available
- If the context doesn't contain relevant information, say so politely
- Keep your answer concise but informative

Answer:"""
        
        # Step 3: Get response from Groq
        messages = [
            SystemMessage(content="You are a helpful study assistant that explains concepts clearly and accurately based on provided study materials."),
            HumanMessage(content=prompt)
        ]
        
        print(f"🤖 Generating answer with Groq...")
        response = self.llm.invoke(messages)
        
        # Store in chat history
        self.chat_history.append({
            'question': question,
            'answer': response.content,
            'context_used': len(results)
        })
        
        return response.content
    
    def get_chat_history(self):
        """Return chat history"""
        return self.chat_history
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        print("✅ Chat history cleared")
