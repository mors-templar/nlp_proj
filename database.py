# database.py

import sqlite3
import datetime
import os

# Define the name of the database file
DB_FILE = "feedback.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS UserSentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment_score REAL NOT NULL,
            sentiment_label TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def insert_feedback(text, score, label):
    conn = get_db_connection()
    cur = conn.cursor()
    ts = datetime.datetime.now().isoformat()
    cur.execute(
        """
        INSERT INTO UserSentiment (text, sentiment_score, sentiment_label, timestamp)
        VALUES (?, ?, ?, ?)
        """, 
        (text, score, label, ts)
    )
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserSentiment ORDER BY timestamp DESC")
    feedback_data = cursor.fetchall()
    conn.close()
    return feedback_data

if not os.path.isfile(DB_FILE):
    create_database()
    print("Database and table created successfully!")
