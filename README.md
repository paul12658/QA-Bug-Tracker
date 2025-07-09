## QA Testing Bug Tracker

A lightweight web-based **Bug Tracking System** built with **Flask**, **SQLite**, and **Jinja2**, designed for QA teams and software testers to efficiently report, manage, and export bugs in software projects.


## 🔧 Features

- ✅ User registration and login system
- 🐞 Submit detailed bug reports with title, description, tag, and status
- 📋 View all reported bugs on a dashboard
- 🏷️ Add tags to categorize bugs (e.g., UI, Backend, API)
- 🔐 Passwords stored securely using hashing (`Werkzeug`)
- 📤 Export bug reports as a downloadable CSV file
- 👨‍💻 Minimal and clean interface using Jinja templates
- 
## 📁 Project Structure

QA-Testing-Bug-Tracker/
├── app.py # Main Flask application
├── bugs.db # SQLite database (auto-created)
├── templates/ # HTML templates
│ ├── login.html
│ ├── register.html
│ ├── index.html
│ └── report.html
├── venv/ # Python virtual environment (optional)
└── README.md # Project documentation

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/qa-bug-tracker.git
cd qa-bug-tracker
## Create Virtual Environment
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
# OR
source venv/bin/activate      # macOS/Linux


## Install dependencies
pip install Flask Flask-SQLAlchemy Werkzeug

## Run App
python app.py


