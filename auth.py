import json  # Importing the JSON module for data serialization and deserialization.
import hashlib  # Importing hashlib module to hash passwords.
import os  # Importing os for operating system related functionality.
from pathlib import Path  # Importing Path from pathlib for file system path manipulation.
from tkinter import messagebox  # Importing messagebox from tkinter to display messages in the GUI.


# Function to get the directory path where application data will be stored.
def get_data_dir():
    home = Path.home()  # Get the user's home directory.

    # If the system is Windows, use a specific path inside the "AppData" directory.
    if os.name == 'nt':
        return home / "AppData" / "Local" / "InsulinTracker"  # Path on Windows.

    # Otherwise, use a hidden directory in the user's home on Unix-based systems.
    return home / ".insulin_tracker"  # Path on non-Windows systems.


# Function to hash the password using SHA-256 encryption.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Hash the password and return it as a hexadecimal string.


# Function to validate a user's login credentials.
def validate_user(username, password):
    data_dir = get_data_dir() / "users"  # Get the path where user data files are stored.
    data_dir.mkdir(parents=True, exist_ok=True)  # Ensure that the "users" directory exists; create it if not.
    user_file = data_dir / f"{hashlib.sha256(username.encode()).hexdigest()}.dat"  # Create a filename based on a hashed username.

    # If the user file doesn't exist, return False indicating invalid credentials.
    if not user_file.exists():
        return False

    try:
        # Try to open the user's data file and load the JSON content.
        with open(user_file, "r") as f:
            user_data = json.load(f)  # Parse the JSON file into a Python dictionary.
            # Check if the provided password matches the stored hashed password.
            return user_data.get("password") == hash_password(password)
    except Exception:
        return False  # In case of any errors (e.g., file read error), return False.


# Function to register a new user.
def register_user(username, password):
    data_dir = get_data_dir() / "users"  # Get the path to the "users" directory.
    data_dir.mkdir(parents=True, exist_ok=True)  # Ensure that the "users" directory exists.
    user_file = data_dir / f"{hashlib.sha256(username.encode()).hexdigest()}.dat"  # Create a filename for the user based on a hashed username.

    # If the user file already exists, return False indicating that the user is already registered.
    if user_file.exists():
        return False

    try:
        # Try to open the user file in write mode and store the username and hashed password as JSON.
        with open(user_file, "w") as f:
            json.dump({
                "username": username,  # Store the username.
                "password": hash_password(password)  # Store the hashed password.
            }, f)
        return True  # Return True indicating successful registration.
    except Exception:
        return False  # In case of any error, return False indicating registration failure.
