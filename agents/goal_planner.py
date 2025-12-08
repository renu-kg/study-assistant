# agents/goal_planner.py
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config.settings import GROQ_API_KEY, GROQ_MODEL
import json
from datetime import datetime, timedelta

class GoalPlannerAgent:
    def __init__(self):
        """Initialize the goal planner agent with Groq LLM"""
        self.llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.3,  # Lower temperature for more structured output
            groq_api_key=GROQ_API_KEY
        )
    
    def create_study_plan(self, goal, deadline, daily_hours, current_knowledge="beginner"):
        """
        Create a structured study plan
        
        Args:
            goal: Main learning objective (e.g., "Master Machine Learning")
            deadline: Target date (string format: "2025-12-31")
            daily_hours: Hours available per day (integer)
            current_knowledge: Current level (beginner/intermediate/advanced)
        
        Returns:
            dict: Structured study plan with subtasks, schedule, and milestones
        """
        
        # Calculate days available
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        today = datetime.now()
        days_available = (deadline_date - today).days
        
        if days_available <= 0:
            return {"error": "Deadline must be in the future"}
        
        total_hours = days_available * daily_hours
        
        # Create prompt for structured plan generation
        prompt = f"""You are an expert study planner. Create a detailed, realistic study plan in JSON format.

Goal: {goal}
Deadline: {deadline} ({days_available} days from now)
Daily Study Hours: {daily_hours}
Total Available Hours: {total_hours}
Current Knowledge Level: {current_knowledge}

Create a comprehensive study plan with:
1. Main goal broken into 5-8 subtasks (topics/chapters)
2. Daily schedule with specific topics for each day
3. Weekly milestones (checkpoints)
4. Recommended resources for each subtask

Return ONLY valid JSON in this exact format:
{{
    "main_goal": "{goal}",
    "total_hours": {total_hours},
    "days_available": {days_available},
    "subtasks": [
        {{
            "task_id": 1,
            "task": "Task name",
            "description": "What to learn",
            "estimated_hours": 10,
            "priority": "high",
            "resources": ["Resource 1", "Resource 2"]
        }}
    ],
    "daily_schedule": [
        {{
            "day": 1,
            "date": "2025-10-31",
            "topics": ["Topic 1", "Topic 2"],
            "duration_hours": {daily_hours},
            "tasks": ["Read Chapter 1", "Complete exercises"]
        }}
    ],
    "milestones": [
        {{
            "milestone": "Complete fundamentals",
            "due_date": "2025-11-07",
            "tasks_to_complete": [1, 2]
        }}
    ]
}}

Make the plan realistic, achievable, and well-structured. Include specific actionable tasks."""

        # Get response from Groq
        messages = [
            SystemMessage(content="You are an expert educational planner who creates realistic, achievable study plans. Always return valid JSON."),
            HumanMessage(content=prompt)
        ]
        
        print(f"🎯 Creating study plan for: {goal}")
        print(f"⏰ Available: {days_available} days, {total_hours} total hours\n")
        
        response = self.llm.invoke(messages)
        
        # Parse JSON response
        try:
            # Extract JSON from response (sometimes LLMs add extra text)
            content = response.content.strip()
            
            # Find JSON block
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            plan = json.loads(content)
            plan['created_at'] = datetime.now().isoformat()
            plan['status'] = 'active'
            
            print("✅ Study plan created successfully!")
            return plan
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing plan: {e}")
            print(f"Response: {response.content[:500]}")
            return {
                "error": "Failed to generate plan",
                "raw_response": response.content
            }
    
    def adapt_plan(self, current_plan, performance_data):
        """
        Adapt study plan based on performance with structured suggestions, hours, and topics.
        Returns dict: {recommendations, adjusted_hours, focus_topics, ...}
        """
        prompt = f"""Based on the current study plan and performance data below, suggest *actionable* study adaptations.
    Current Plan Summary:
    - Goal: {current_plan.get('main_goal', 'N/A')}
    - Progress: {len(performance_data.get('quiz_scores', []))} quizzes completed

    Performance Data:
    {json.dumps(performance_data, indent=2)}

    Provide your answer in JSON with these keys:
    - recommendations: ["Tip 1", "Tip 2", ...]
    - adjusted_hours: [{{"topic": ..., "current_hours": ..., "recommended_hours": ...}}, ...]
    - focus_topics: ["topic1", "topic2", ...]
    - motivational_tips: ["tip1", "tip2", ...]

    Example:
    {{
    "recommendations": ["Review Java basics", "Add 2 hours to topic X"],
    "adjusted_hours": [{{"topic": "Java Inheritance", "current_hours": 4, "recommended_hours": 7}}],
    "focus_topics": ["Java Inheritance", "Polymorphism"],
    "motivational_tips": ["You're making progress!", "Keep practicing on weak areas"]
    }}

    DO NOT return markdown or code, just valid JSON.
    """

        messages = [
            SystemMessage(content="You are an adaptive learning coach who gives specific, structured recommendations in JSON."),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        content = response.content.strip()
        # Extract JSON from response (even if LLM wraps in markdown)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        try:
            adaptations = json.loads(content)
            adaptations['adapted_at'] = datetime.now().isoformat()
            return adaptations
        except Exception:
            return {
                "recommendations": [response.content.strip()],
                "adapted_at": datetime.now().isoformat()
            }
