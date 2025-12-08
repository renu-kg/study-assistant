# utils/reminder_manager.py - PERSISTENT REMINDERS VERSION
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import json
import os

class ReminderManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.jobs = []
        self.active_notifications = []  # Store active notifications

    # === Core Reminder Methods ===

    def add_reminder(self, task_name, run_datetime, callback=None):
        """Schedule a one-time reminder"""
        trigger = CronTrigger(
            year=run_datetime.year,
            month=run_datetime.month,
            day=run_datetime.day,
            hour=run_datetime.hour,
            minute=run_datetime.minute
        )
        # Wrapper function to add notification
        def notify_wrapper(task):
            notification = {
                "task": task,
                "time": datetime.now().isoformat(),
                "message": f"⏰ Time to: {task}"
            }
            self.active_notifications.append(notification)
            print(f"🛎️ [REMINDER]: {task}")
            if callback:
                callback(task)
        job = self.scheduler.add_job(notify_wrapper, trigger=trigger, args=[task_name])
        self.jobs.append(job)
        print(f"✅ Reminder set for '{task_name}' at {run_datetime}")
        return job

    def add_daily_reminder(self, task_name, hour, minute, callback=None):
        """Schedule a recurring daily reminder"""
        trigger = CronTrigger(hour=hour, minute=minute)
        def notify_wrapper(task):
            notification = {
                "task": task,
                "time": datetime.now().isoformat(),
                "message": f"⏰ Daily reminder: {task}"
            }
            self.active_notifications.append(notification)
            if callback:
                callback(task)
        job = self.scheduler.add_job(notify_wrapper, trigger=trigger, args=[task_name])
        self.jobs.append(job)
        print(f"✅ Daily reminder set for '{task_name}' at {hour:02d}:{minute:02d}")
        return job

    def get_active_notifications(self):
        """Get unread notifications"""
        return self.active_notifications

    def clear_notification(self, index):
        """Clear a specific notification"""
        if 0 <= index < len(self.active_notifications):
            self.active_notifications.pop(index)

    def clear_all_notifications(self):
        """Clear all notifications"""
        self.active_notifications = []

    def list_reminders(self):
        jobs = self.scheduler.get_jobs()
        if not jobs:
            print("- No reminders set.")
            return
        for job in jobs:
            print(f"- {job.args[0] if job.args else 'Unknown'}, next run at {job.next_run_time}")

    def remove_all(self):
        """Remove all reminders"""
        for job in self.scheduler.get_jobs():
            job.remove()
        self.jobs = []
        print("❌ All reminders cleared.")

    def shutdown(self):
        self.scheduler.shutdown()

    # === Persistence Methods ===

    def save_scheduled_reminders(self, user_id, reminders):
        """Save all scheduled reminders to disk (JSON)"""
        path = f"data/user_data/{user_id}_reminders.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(reminders, f, indent=2)

    def load_scheduled_reminders(self, user_id):
        """Load reminders from disk (JSON file)"""
        path = f"data/user_data/{user_id}_reminders.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []

    def schedule_reminders_from_file(self, user_id, callback=None):
        """Re-schedule all reminders from disk (call after login/start)"""
        reminders = self.load_scheduled_reminders(user_id)
        for r in reminders:
            dt = datetime.fromisoformat(r['datetime'])
            self.add_reminder(r['message'], dt, callback)
