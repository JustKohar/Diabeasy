import json
import os

def load_user_data(username):
    filename = f"{username}_data.json"
    if not os.path.exists(filename):
        return []
        
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_user_data(username, data):
    with open(f"{username}_data.json", "w") as f:
        json.dump(data, f, indent=4)