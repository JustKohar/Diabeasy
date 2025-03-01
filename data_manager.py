import json
from cryptography.fernet import Fernet
import base64
import hashlib
from pathlib import Path
import os

SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"InsulinTrackerSecureKey123").digest())

def get_data_dir():
    home = Path.home()
    if os.name == 'nt':
        return home / "AppData" / "Local" / "InsulinTracker"
    return home / ".insulin_tracker"

def encrypt_data(data):
    fernet = Fernet(SECRET_KEY)
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted):
    fernet = Fernet(SECRET_KEY)
    return json.loads(fernet.decrypt(encrypted).decode())

def save_user_data(username, data_type, data):
    user_dir = get_data_dir() / "data" / hashlib.sha256(username.encode()).hexdigest()
    user_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(user_dir / f"{data_type}.dat", "wb") as f:
            f.write(encrypt_data(data))
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def load_user_data(username, data_type):
    user_dir = get_data_dir() / "data" / hashlib.sha256(username.encode()).hexdigest()
    file_path = user_dir / f"{data_type}.dat"
    
    if not file_path.exists():
        return None
        
    try:
        with open(file_path, "rb") as f:
            return decrypt_data(f.read())
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None