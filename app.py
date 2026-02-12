from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from modules.ocr_engine import extract_text_from_image
from modules.parser import parse_transactions
from modules.fraud_detection import detect_fraud

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            debit REAL,
            credit REAL,
            balance REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text_from_image(path)
    transactions = parse_transactions(text)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for txn in transactions:
        cursor.execute("""
            INSERT INTO transactions (date, description, debit, credit, balance)
            VALUES (?, ?, ?, ?, ?)
        """, (txn["date"], txn["description"], txn["debit"],
              txn["credit"], txn["balance"]))

    conn.commit()
    conn.close()

    frauds = detect_fraud(transactions)

    return jsonify({
        "transactions": transactions,
        "frauds": frauds
    })

@app.route("/summary")
def summary():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(debit), SUM(credit) FROM transactions")
    result = cursor.fetchone()

    cursor.execute("SELECT date, debit FROM transactions")
    data = cursor.fetchall()

    conn.close()

    return jsonify({
        "total_debit": result[0] or 0,
        "total_credit": result[1] or 0,
        "monthly_data": data
    })

if __name__ == "__main__":
    app.run(debug=True)
