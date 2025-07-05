import sqlite3
import os

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Connect to SQLite DB
conn = sqlite3.connect("data/expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    notes TEXT
)
""")
conn.commit()

def add_expense(amount, category, date, notes):
    cursor.execute("INSERT INTO expenses (amount, category, date, notes) VALUES (?, ?, ?, ?)",
                   (amount, category, date, notes))
    conn.commit()

def get_all_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    return cursor.fetchall()

def delete_expense(expense_id):
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

