# Insulin Tracker Application

A Python-based application for tracking insulin usage, calculating doses, and maintaining a secure history of treatments.

## Features
- **User Authentication**: Secure login and registration system
- **Insulin Calculation**: Automatic dose calculation based on blood sugar levels
- **History Tracking**: Maintains a secure, encrypted history of all calculations
- **Profile Management**: Customizable insulin profiles for different times of day
- **Data Export**: Generate PDF reports of treatment history
- **Responsive UI**: Clean, modern interface with intuitive controls
- **EXE**: There is an exe able to download on computer for easy use

## Requirements

### Python Packages
Install the required Python packages using pip:
```bash
pip install cryptography pdfkit

### wkhtmltopdf Installs: : Required for PDF generation
Windows: Download from wkhtmltopdf.org
macOS: brew install wkhtmltopdf
Linux: sudo apt-get install wkhtmltopdf


### HOW TO CLONE
git clone https://github.com/JustKohar/Hackathon-Year-2.git
cd Hackathon-Year-2

### TO RUN
python main.py

### FILE STRUCTURE
insulin-tracker/
├── main.py              # Application entry point
├── auth.py              # Authentication handling
├── data_manager.py      # Secure data storage
├── gui.py               # Main application interface
├── profile_manager.py   # Insulin profile management
├── history.py           # History tracking and display
├── login_image.png      # Login screen image
└── README.md            # This file
----------------------------------------------------------
Usage
Login Screen
Username: Enter your registered username

Password: Enter your password

Register: Create a new account if you don't have one

Main Application
Profile Setup: Configure your insulin profile

Calculator: Enter current blood sugar and time for dose calculation

History: View and manage treatment history

Logout: Securely end your session

Data Security
All user data is encrypted using AES-256

Passwords are hashed using SHA-256

Data files are stored in system-specific secure locations

Reporting Issues
Please report any issues via GitHub Issues with:

Detailed description of the problem

Steps to reproduce