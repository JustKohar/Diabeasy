import json
import hashlib
import os
from pathlib import Path
from tkinter import messagebox

def get_data_dir():
    home = Path.home()
    if os.name == 'nt':
        return home / "AppData" / "Local" / "InsulinTracker"
    return home / ".insulin_tracker"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_user(username, password):
    data_dir = get_data_dir() / "users"
    data_dir.mkdir(parents=True, exist_ok=True)
    user_file = data_dir / f"{hashlib.sha256(username.encode()).hexdigest()}.dat"
    
    if not user_file.exists():
        return False
        
    try:
        with open(user_file, "r") as f:
            user_data = json.load(f)
            return user_data.get("password") == hash_password(password)
    except Exception:
        return False

def register_user(username, password):
    data_dir = get_data_dir() / "users"
    data_dir.mkdir(parents=True, exist_ok=True)
    user_file = data_dir / f"{hashlib.sha256(username.encode()).hexdigest()}.dat"
    
    if user_file.exists():
        return False
        
    try:
        with open(user_file, "w") as f:
            json.dump({
                "username": username,
                "password": hash_password(password)
            }, f)
        return True
    except Exception:
        return False