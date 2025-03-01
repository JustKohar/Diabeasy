import json
import hashlib
import os
from tkinter import messagebox

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return False
            
        users[username] = hash_password(password)
        save_users(users)
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")
        return False

def authenticate(username, password):
    try:
        users = load_users()
        return users.get(username) == hash_password(password)
    except Exception as e:
        messagebox.showerror("Error", f"Login failed: {str(e)}")
        return False

def load_users():
    if not os.path.exists("users.json"):
        return {}
        
    with open("users.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)