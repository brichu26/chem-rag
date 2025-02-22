import sqlite3
import pandas as pd

# Sample medical data
data = [
    ("Heart Disease", "Heart disease includes conditions that affect the heart's function."),
    ("Diabetes", "Diabetes is a chronic condition that affects blood sugar regulation."),
    ("Hypertension", "Hypertension is high blood pressure that can lead to heart problems."),
    ("COVID-19", "COVID-19 is caused by SARS-CoV-2, affecting the respiratory system."),
]

# Connect to SQLite database
conn = sqlite3.connect("medical.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition TEXT,
        description TEXT
    )
""")

# Insert data
cursor.executemany("INSERT INTO medical_records (condition, description) VALUES (?, ?)", data)

# Commit and close
conn.commit()
conn.close()
