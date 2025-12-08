# agents/performance_tracker.py
import json
import os
from datetime import datetime
from collections import defaultdict

class PerformanceTracker:
    def __init__(self, user_id="default_user"):
        """Initialize performance tracker"""
        self.user_id = user_id
        self.data_file = f"data/user_data/{user_id}_performance.json"
        self.performance_data = self.load_performance_data()
    
    def load_performance_data(self):
        """Load existing performance data or create new"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "quiz_scores": [],
                "completed_tasks": [],
                "study_sessions": [],
                "weak_topics": [],
                "created_at": datetime.now().isoformat()
            }
    
    def save_performance_data(self):
        """Save performance data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.performance_data, f, indent=2)
        print(f"💾 Performance data saved to {self.data_file}")
    
    def record_quiz_score(self, topic, score, max_score=100):
        """
        Record a quiz score
        
        Args:
            topic: Quiz topic/subject
            score: Points scored
            max_score: Maximum possible points
        """
        percentage = (score / max_score) * 100
        
        quiz_entry = {
            "topic": topic,
            "score": score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "date": datetime.now().isoformat(),
            "status": "pass" if percentage >= 70 else "needs_improvement"
        }
        
        self.performance_data["quiz_scores"].append(quiz_entry)
        
        # Update weak topics if score < 70%
        if percentage < 70:
            if topic not in self.performance_data["weak_topics"]:
                self.performance_data["weak_topics"].append(topic)
        else:
            # Remove from weak topics if improved
            if topic in self.performance_data["weak_topics"]:
                self.performance_data["weak_topics"].remove(topic)
        
        self.save_performance_data()
        print(f"✅ Quiz score recorded: {topic} - {percentage}%")
        
        return quiz_entry
    
    def record_task_completion(self, task_id, task_name, time_spent_hours):
        """Record completed task"""
        task_entry = {
            "task_id": task_id,
            "task_name": task_name,
            "time_spent_hours": time_spent_hours,
            "completed_at": datetime.now().isoformat()
        }
        
        self.performance_data["completed_tasks"].append(task_entry)
        self.save_performance_data()
        print(f"✅ Task completed: {task_name}")
        
        return task_entry
    
    def record_study_session(self, duration_minutes, topics_covered):
        """Record study session"""
        session_entry = {
            "duration_minutes": duration_minutes,
            "topics_covered": topics_covered,
            "date": datetime.now().isoformat()
        }
        
        self.performance_data["study_sessions"].append(session_entry)
        self.save_performance_data()
        
        return session_entry
    
    def get_topic_performance(self):
        """Get performance summary by topic"""
        topic_scores = defaultdict(list)
        
        for quiz in self.performance_data["quiz_scores"]:
            topic_scores[quiz["topic"]].append(quiz["percentage"])
        
        # Calculate average per topic
        topic_summary = {}
        for topic, scores in topic_scores.items():
            topic_summary[topic] = {
                "average_score": round(sum(scores) / len(scores), 2),
                "attempts": len(scores),
                "latest_score": scores[-1],
                "trend": "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable"
            }
        
        return topic_summary
    
    def get_weak_topics(self):
        """Get list of topics needing improvement"""
        return self.performance_data["weak_topics"]
    
    def get_completion_rate(self, total_tasks):
        """Calculate task completion rate"""
        completed = len(self.performance_data["completed_tasks"])
        rate = (completed / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "completed": completed,  # ✅ Changed from "completed_tasks"
            "total": total_tasks,    # ✅ Changed from "total_tasks"
            "pending": total_tasks - completed,
            "completion_rate": round(rate, 2)
        }
    
    def get_study_time_stats(self):
        """Get study time statistics"""
        sessions = self.performance_data["study_sessions"]
        
        if not sessions:
            return {
                "total_hours": 0,
                "total_sessions": 0,
                "average_session_minutes": 0
            }
        
        total_minutes = sum(s["duration_minutes"] for s in sessions)
        
        return {
            "total_hours": round(total_minutes / 60, 2),
            "total_sessions": len(sessions),
            "average_session_minutes": round(total_minutes / len(sessions), 2)
        }
    
    def generate_performance_report(self, total_tasks=10):
        """Generate comprehensive performance report"""
        report = {
            "user_id": self.user_id,
            "report_date": datetime.now().isoformat(),
            "quiz_performance": self.get_topic_performance(),
            "weak_topics": self.get_weak_topics(),
            "completion_stats": self.get_completion_rate(total_tasks),
            "study_time": self.get_study_time_stats(),
            "total_quizzes": len(self.performance_data["quiz_scores"]),
            "recommendations": self.get_recommendations()
        }
        
        return report
    
    def get_recommendations(self):
        """Generate study recommendations based on performance"""
        recommendations = []
        
        # Check weak topics
        weak = self.get_weak_topics()
        if weak:
            recommendations.append(f"Focus on improving: {', '.join(weak)}")
            recommendations.append("Consider revisiting fundamentals for weak topics")
        
        # Check study time
        stats = self.get_study_time_stats()
        if stats["total_sessions"] > 0 and stats["average_session_minutes"] < 30:
            recommendations.append("Try longer study sessions (45-60 minutes) for better retention")
        
        # Check quiz performance
        topic_perf = self.get_topic_performance()
        if topic_perf:
            avg_scores = [data["average_score"] for data in topic_perf.values()]
            overall_avg = sum(avg_scores) / len(avg_scores)
            
            if overall_avg < 70:
                recommendations.append("Consider slowing down pace to improve understanding")
            elif overall_avg > 85:
                recommendations.append("Great progress! Consider advancing to more challenging topics")
        
        if not recommendations:
            recommendations.append("Keep up the good work! Stay consistent.")
        
        return recommendations
    
    def clear_data(self):
        """Clear all performance data (for testing)"""
        self.performance_data = {
            "quiz_scores": [],
            "completed_tasks": [],
            "study_sessions": [],
            "weak_topics": [],
            "created_at": datetime.now().isoformat()
        }
        self.save_performance_data()
        print("🗑️ Performance data cleared")
