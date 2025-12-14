# 🎯 Goal-Oriented Virtual Study Assistant

An AI-powered study assistant designed to help students plan, organize, and manage their studies efficiently using **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**.

This project provides personalized study planning, AI-based concept explanations, automatic quiz generation, performance tracking, and smart reminders — all in one platform.

---

## 🚀 Features

- 📚 Upload study materials (PDF / TXT)
- 🧠 AI-based concept explanation using RAG
- 📝 Automatic quiz generation from uploaded content
- 📊 Performance tracking & weak-topic analysis
- 🎯 Personalized goal-oriented study planning
- ⏰ Task management & smart reminders
- 🖥️ Clean and interactive UI using Streamlit

---

## 🧠 Technologies Used

- **Python**
- **Streamlit**
- **LangChain**
- **Groq LLM API (GPT-4 class model)**
- **FAISS (Vector Database)**
- **APScheduler (Reminders)**
- **PDF/Text Processing Libraries**

---

## ⚙️ Setup Instructions

1. Clone or unzip the repository:
   ```bash
   git clone https://github.com/renu-kg/study-assistant.git
   cd study-assistant

2. Create a virtual environment:
   python -m venv venv

3. Activate the environment:
   - On Windows: venv\Scripts\activate 
   - On Mac/Linux: source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create a .env file and add your Groq API Key:
   GROQ_API_KEY=your_api_key_here

6. Run the application:
   streamlit run app.py

---

## 🧠 Project Concept

The **Goal-Oriented Virtual Study Assistant** is designed to bridge the gap between traditional study methods and modern AI-driven personalized learning systems.

Instead of acting like a generic chatbot, the system:
- Understands **user-uploaded study material**
- Creates **personalized study plans**
- Tracks **learning performance**
- Adapts suggestions based on weak areas
- Keeps students consistent using **smart reminders**

The core idea is to help students not only *learn content*, but also *plan, revise, and improve continuously* with AI assistance.

---

## 🔍 How RAG Works in This Project

**RAG (Retrieval-Augmented Generation)** is used to ensure that AI responses are **accurate, context-aware, and based on the student’s own study material**, rather than generic internet knowledge.

### Step-by-step Flow:

1. **Material Upload**
   - The user uploads a PDF or text file.
   - Text is extracted from the document.

2. **Chunking**
   - The text is split into small, meaningful chunks.
   - This improves retrieval accuracy and performance.

3. **Embedding Generation**
   - Each chunk is converted into a numerical vector (embedding).
   - These embeddings capture the semantic meaning of the text.

4. **Vector Storage (FAISS)**
   - All embeddings are stored in a FAISS vector database.
   - FAISS enables fast similarity-based search.

5. **Query & Retrieval**
   - When the user asks a question or requests a quiz:
     - The query is converted into an embedding.
     - FAISS retrieves the most relevant chunks.

6. **LLM Response Generation**
   - Retrieved context + user query is passed to the LLM via LangChain.
   - The LLM generates a precise, context-based answer or quiz.

### Why RAG?

- Prevents hallucinations
- Ensures answers come from **user-provided content**
- Improves accuracy and trustworthiness
- Scales well for large documents

---

## 🧩 Key Modules Implemented

- **GoalPlannerAgent**  
  Creates personalized study plans based on deadlines, available days, and proficiency.

- **ConceptExplainerAgent (RAG-based)**  
  Answers questions using uploaded study material.

- **QuizGenerator**  
  Automatically generates MCQs from documents.

- **PerformanceTracker**  
  Analyzes quiz results and identifies weak topics.

- **TodoManager**  
  Converts study plans into actionable tasks.

- **ReminderManager**  
  Sends notifications for tasks, sessions, and deadlines.

---

## 🤖 AI & Technologies Used

- **Generative AI** – For explanations, planning, and quiz generation
- **RAG (Retrieval-Augmented Generation)** – Context-based learning
- **LangChain** – LLM orchestration
- **Groq LLM API** – High-speed GPT-4 class inference
- **FAISS** – Vector similarity search
- **Streamlit** – Frontend UI
- **Python** – Core backend implementation

---

## 👥 Team Members

| Name                  | USN         |
|-----------------------|-------------|
| Pavan Kumar Hiremath  | 4BD23CS153  |
| Renu K G              | 4BD23CS169  |
| Sachin M H            | 4BD23CS181  |
| Sakshi P B            | 4BD23CS183  |

---

## 🔮 Future Enhancements

- Adaptive learning using long-term performance trends
- Spaced repetition scheduling
- Calendar and WhatsApp notification integration
- Voice-based interaction
- Multimodal RAG (images, handwritten notes)
- Mobile application support
- Advanced analytics dashboard for learning insights

---

## 📌 Conclusion

The Goal-Oriented Virtual Study Assistant demonstrates how **AI, RAG, and intelligent planning** can be combined to create a practical, student-focused learning system.  
By integrating personalized planning, context-aware explanations, and performance-driven feedback, the system promotes consistent learning and better academic outcomes.

---

## 📬 Contact

📧 kgrenu1@gmail.com

