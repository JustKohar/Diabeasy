# data_manager.py
import json
import os
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
import base64

# Generate secret key (add hashlib import)
SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"YourAppName123").digest())

def get_data_dir():
    """Get OS-specific hidden data directory"""
    home = Path.home()
    if os.name == 'nt':
        return home / "AppData" / "Local" / "InsulinTracker"
    else:
        return home / ".insulin_tracker"

def ensure_data_dir():
    """Create data directory if missing"""
    data_dir = get_data_dir()
    data_dir.mkdir(exist_ok=True, parents=True)
    return data_dir

def get_user_path(username):
    """Get hashed user data path"""
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    return get_data_dir() / f"{username_hash}.dat"

def encrypt_data(data):
    fernet = Fernet(SECRET_KEY)
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data):
    fernet = Fernet(SECRET_KEY)
    return json.loads(fernet.decrypt(encrypted_data).decode())

def load_user_data(username):
    data_file = get_user_path(username)
    if not data_file.exists():
        return []
    
    try:
        with open(data_file, "rb") as f:
            return decrypt_data(f.read())
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return []

def save_user_data(username, data):
    try:
        ensure_data_dir()
        data_file = get_user_path(username)
        with open(data_file, "wb") as f:
            f.write(encrypt_data(data))
    except Exception as e:
        print(f"Error saving data: {str(e)}")