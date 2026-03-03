## 🌍 Live Demo
https://your-render-url.onrender.com

# 📊 SentimentAI – Feedback Sentiment Dashboard

SentimentAI is a Flask-based web application that analyzes textual feedback and classifies it as Positive, Negative, or Neutral using Natural Language Processing.

This project was built to explore practical NLP implementation, database integration, authentication systems, and dashboard-style UI development in a full-stack environment.

---

## 🚀 What This Project Does

- Allows an admin to securely log in  
- Accepts textual feedback input  
- Analyzes sentiment using VADER (NLTK)  
- Stores feedback and results in a SQLite database  
- Displays real-time sentiment statistics  
- Visualizes distribution using a pie chart  
- Enables filtering of feedback by sentiment  
- Allows exporting data as CSV  
- Provides delete functionality for data management  

---

## 🛠 Technologies Used

- Python (Flask)
- SQLite
- NLTK – VADER Sentiment Analyzer
- Matplotlib
- HTML & CSS (custom glassmorphism design)

---

## 🧠 Project Overview

After logging in, the admin can submit feedback text.  
The system processes the input using VADER sentiment analysis and calculates a compound score to determine whether the feedback is Positive, Negative, or Neutral.

Each entry is stored in the database and reflected in the dashboard statistics. The dashboard dynamically updates total counts and sentiment distribution.

Data can be filtered, deleted, or exported when required.

---

## 📦 Running the Project Locally

Clone the repository and set up the virtual environment:

```bash
git clone <your-repo-url>
cd feedback-sentiment-analyzer
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py

Then open:

http://127.0.0.1:5000

Default login credentials:

-Username: admin
-Password: admin123

📌 Notes

This project was built as a portfolio mini-project to demonstrate:
    ->Backend development with Flask
    ->Database handling using SQLite
    ->Integration of NLP techniques
    ->Dashboard UI design
    ->Authentication and session management

| Future improvements may include multi-user roles, faculty-wise analysis, trend tracking, and deployment to cloud platforms. |

