import json  # Importing the JSON module to handle data serialization and deserialization.
from cryptography.fernet import Fernet  # Importing Fernet for symmetric encryption/decryption.
import base64  # Importing base64 to handle URL-safe base64 encoding.
import hashlib  # Importing hashlib for creating cryptographic hashes.
from pathlib import Path  # Importing Path from pathlib for easier handling of file system paths.
import os  # Importing os to interact with the operating system, such as checking paths.

# Generate a secret encryption key by hashing a hardcoded string and encoding it in base64 format.
# This secret key is used for Fernet encryption to secure data.
SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"InsulinTrackerSecureKey123").digest())


# Function to determine and return the directory where the application data will be stored.
def get_data_dir():
    home = Path.home()  # Get the user's home directory.

    # If the operating system is Windows, use the "AppData" directory to store data.
    if os.name == 'nt':
        return home / "AppData" / "Local" / "InsulinTracker"  # Path on Windows.

    # Otherwise, on Unix-based systems (Linux/macOS), store data in a hidden directory within the user's home.
    return home / ".insulin_tracker"  # Path on Unix-like systems.


# Function to encrypt data using Fernet encryption with the generated secret key.
def encrypt_data(data):
    fernet = Fernet(SECRET_KEY)  # Initialize the Fernet object with the secret key.
    # Convert the data into a JSON string, then encode it into bytes, and encrypt the byte data.
    return fernet.encrypt(json.dumps(data).encode())


# Function to decrypt data using Fernet decryption with the same secret key.
def decrypt_data(encrypted):
    fernet = Fernet(SECRET_KEY)  # Initialize the Fernet object with the secret key.
    # Decrypt the encrypted data and decode it into a JSON string, then parse it back into a Python dictionary.
    return json.loads(fernet.decrypt(encrypted).decode())


# Function to save encrypted user data to a file.
def save_user_data(username, data_type, data):
    # Create a directory for the user by hashing the username to ensure a unique folder.
    user_dir = get_data_dir() / "data" / hashlib.sha256(username.encode()).hexdigest()
    user_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist.

    try:
        # Open the appropriate file for the given data type (e.g., "user_profile.dat") and write the encrypted data.
        with open(user_dir / f"{data_type}.dat", "wb") as f:
            f.write(encrypt_data(data))  # Encrypt the data and write it to the file.
    except Exception as e:
        # If an error occurs during the saving process, print the error message.
        print(f"Error saving data: {str(e)}")


# Function to load and decrypt user data from a file.
def load_user_data(username, data_type):
    # Create a directory for the user by hashing the username (same as in saving).
    user_dir = get_data_dir() / "data" / hashlib.sha256(username.encode()).hexdigest()
    file_path = user_dir / f"{data_type}.dat"  # Build the file path based on the data type (e.g., "user_profile.dat").

    # If the file doesn't exist, return None (indicating no data was found).
    if not file_path.exists():
        return None

    try:
        # Open the file and read the encrypted data, then decrypt it.
        with open(file_path, "rb") as f:
            return decrypt_data(f.read())  # Decrypt the data and return it.
    except Exception as e:
        # If an error occurs during the loading process, print the error message and return None.
        print(f"Error loading data: {str(e)}")
        return None  # Return None if any error occurs during decryption or file reading.
