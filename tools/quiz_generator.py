# tools/quiz_generator.py
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config.settings import GROQ_API_KEY, GROQ_MODEL
import json
import datetime

class QuizGenerator:
    def __init__(self, vector_store):
        self.llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.3,
            groq_api_key=GROQ_API_KEY
        )
        self.vector_store = vector_store
    
    def generate_quiz(self, topic, num_questions=5, difficulty="medium"):
        """
        Generate quiz questions from study material
        
        Args:
            topic: Topic to generate quiz about
            num_questions: Number of questions (default: 5)
            difficulty: easy/medium/hard
        
        Returns:
            dict: Quiz with questions, options, and answers
        """
        # Retrieve relevant content
        from utils.vector_store import search_vector_store
        results = search_vector_store(self.vector_store, topic, k=5)
        context = "\n\n".join([doc.page_content for doc in results])
        
        prompt = f"""You are a quiz generator. Create a multiple-choice quiz based on the following study material.

Study Material:
{context}

Generate {num_questions} multiple-choice questions about {topic}.
Difficulty level: {difficulty}

Return ONLY valid JSON in this format:
{{
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "id": 1,
            "question": "Question text here?",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Why this is correct"
        }}
    ]
}}

Make questions clear, relevant to the study material, and appropriately challenging."""

        messages = [
            SystemMessage(content="You are an expert educational quiz generator. Always return valid JSON."),
            HumanMessage(content=prompt)
        ]
        
        print(f"🎯 Generating {num_questions} quiz questions about {topic}...")
        response = self.llm.invoke(messages)
        
        try:
            content = response.content.strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            quiz = json.loads(content)
            quiz['generated_at'] = datetime.datetime.now().isoformat()
            
            print(f"✅ Quiz generated successfully!")
            return quiz
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing quiz: {e}")
            print(f"Response content: {response.content[:500]}")
            return {
                "error": "Failed to generate quiz",
                "raw_response": response.content
            }
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {
                "error": str(e),
                "raw_response": response.content if hasattr(response, 'content') else "No response"
            }
