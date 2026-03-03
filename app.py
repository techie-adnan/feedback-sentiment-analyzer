from flask import Flask, render_template, request, redirect, url_for, session, Response
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import os
import sqlite3

nltk.download('vader_lexicon')

app = Flask(__name__)
app.secret_key = "supersecretkey"

sia = SentimentIntensityAnalyzer()


# -----------------------
# DATABASE SETUP
# -----------------------
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sentiment TEXT,
            score REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -----------------------
# LOGIN ROUTE
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# -----------------------
# LOGOUT ROUTE
# -----------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# -----------------------
# MAIN DASHBOARD ROUTE
# -----------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if not session.get("admin"):
        return redirect(url_for("login"))

    sentiment = None
    score = None
    chart_path = None

    if request.method == "POST":
        feedback = request.form["feedback"]

        result = sia.polarity_scores(feedback)
        score = result["compound"]

        if score >= 0.05:
            sentiment = "Positive"
        elif score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        conn = sqlite3.connect("feedback.db")
        c = conn.cursor()
        c.execute("INSERT INTO feedback (text, sentiment, score) VALUES (?, ?, ?)",
                  (feedback, sentiment, score))
        conn.commit()
        conn.close()

    # Fetch sentiment counts
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("SELECT sentiment FROM feedback")
    data = c.fetchall()
    conn.close()

    sentiment_counts = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    for row in data:
        sentiment_counts[row[0]] += 1

    total = len(data)
    positive_count = sentiment_counts["Positive"]
    negative_count = sentiment_counts["Negative"]
    neutral_count = sentiment_counts["Neutral"]

    # Generate chart
    if total > 0:
        labels = sentiment_counts.keys()
        values = sentiment_counts.values()

        plt.figure()
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Sentiment Distribution")

        chart_path = os.path.join("static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

    # Filtering
    filter_type = request.args.get("filter", "All")

    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()

    if filter_type == "All":
        c.execute("SELECT id, text, sentiment, score FROM feedback ORDER BY id DESC")
    else:
        c.execute("SELECT id, text, sentiment, score FROM feedback WHERE sentiment=? ORDER BY id DESC",
                  (filter_type,))

    history = c.fetchall()
    conn.close()

    return render_template("index.html",
                           sentiment=sentiment,
                           score=score,
                           chart_path=chart_path,
                           history=history,
                           total=total,
                           positive_count=positive_count,
                           negative_count=negative_count,
                           neutral_count=neutral_count,
                           filter_type=filter_type)

@app.route("/delete/<int:feedback_id>")
def delete(feedback_id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# -----------------------
# EXPORT ROUTE
# -----------------------
@app.route("/export")
def export():

    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("SELECT text, sentiment, score FROM feedback")
    data = c.fetchall()
    conn.close()

    def generate():
        yield "Feedback,Sentiment,Score\n"
        for row in data:
            yield f'"{row[0]}",{row[1]},{row[2]}\n'

    return Response(generate(),
                    mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=feedback_data.csv"})


if __name__ == "__main__":
    app.run(debug=True)