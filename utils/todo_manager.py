# utils/todo_manager.py - FIXED VERSION
import json
import os
import uuid
from datetime import datetime

class TodoManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.todo_file = f"data/user_data/{user_id}_todos.json"
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Load user's todo list"""
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r') as f:
                return json.load(f)
        return {"tasks": []}
    
    def save_todos(self):
        """Save todo list"""
        os.makedirs(os.path.dirname(self.todo_file), exist_ok=True)
        with open(self.todo_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
        print(f"✅ Saved todos to {self.todo_file}")
    
    def add_task(self, task_name, estimated_hours, priority="medium"):
        """Add new task"""
        task = {
            "id": str(uuid.uuid4()),
            "name": task_name,
            "estimated_hours": estimated_hours,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.todos["tasks"].append(task)
        self.save_todos()
        return task
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        for task in self.todos["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_todos()
                return True
        return False
    
    def get_pending_tasks(self):
        """Get all pending tasks"""
        return [t for t in self.todos["tasks"] if not t["completed"]]
    
    def get_completed_tasks(self):
        """Get all completed tasks"""
        return [t for t in self.todos["tasks"] if t["completed"]]
    
    def get_completion_stats(self):
        """Get completion statistics"""
        total = len(self.todos["tasks"])
        completed = len(self.get_completed_tasks())
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "percentage": round((completed / total * 100) if total > 0 else 0, 2)
        }
    
    def import_from_study_plan(self, plan):
        """Import tasks from study plan - FIXED VERSION"""
        imported_count = 0
        
        for subtask in plan.get('subtasks', []):
            # Check if task already exists to avoid duplicates
            task_exists = any(
                t['name'] == subtask['task'] 
                for t in self.todos["tasks"]
            )
            
            if not task_exists:
                self.add_task(
                    task_name=subtask['task'],
                    estimated_hours=subtask['estimated_hours'],
                    priority=subtask['priority']
                )
                imported_count += 1
        
        print(f"✅ Imported {imported_count} tasks from study plan")
        return imported_count

    def delete_task(self, task_id):
        self.todos["tasks"] = [t for t in self.todos["tasks"] if t["id"] != task_id]
        self.save_todos()
