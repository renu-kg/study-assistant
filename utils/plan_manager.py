import glob
import os
import json
from datetime import datetime   


def list_user_plans(username):
    """Return list of user's saved plan files (filename, readable_label)"""
    files = glob.glob(f"data/user_data/{username}_plan_*.json")
    plans = []
    for path in sorted(files, reverse=True):
        basename = os.path.basename(path)
        label = basename.replace(f"{username}_plan_", "").replace(".json", "")
        plans.append((basename, label))
    return plans

def load_plan_from_file(username, filename):
    path = f"data/user_data/{filename}"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def delete_plan_file(username, filename):
    path = f"data/user_data/{filename}"
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
