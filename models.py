import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('db/finance_tracker.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    financial_goals TEXT,
    monthly_income REAL,
    income_frequency TEXT,
    expense_categories TEXT,
    financial_priorities TEXT
)
''')

# Create Transaction table
cursor.execute('''
CREATE TABLE IF NOT EXISTS "Transaction" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_TIMESTAMP,
    category TEXT,
    description TEXT,
    amount REAL,
    type TEXT,
    FOREIGN KEY (user_id) REFERENCES User (id)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

# Define User and Transaction classes if needed for further abstraction
class User:
    def __init__(self, username, financial_goals=None, monthly_income=None,
                 income_frequency=None, expense_categories=None, financial_priorities=None):
        self.username = username
        self.financial_goals = financial_goals
        self.monthly_income = monthly_income
        self.income_frequency = income_frequency
        self.expense_categories = expense_categories
        self.financial_priorities = financial_priorities

class Transaction:
    def __init__(self, user_id, category, description, amount, type, date=None):
        self.user_id = user_id
        self.category = category
        self.description = description
        self.amount = amount
        self.type = type
        if date:
            self.date = date
        else:
            self.date = datetime.utcnow()  # Default to current datetime

    def save(self):
        conn = sqlite3.connect('db/finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO "Transaction" (user_id, category, description, amount, type, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.category, self.description, self.amount, self.type, self.date))
        conn.commit()
        conn.close()

    @staticmethod
    def get_transactions(user_id):
        conn = sqlite3.connect('db/finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM "Transaction" WHERE user_id = ?
        ''', (user_id,))
        transactions = cursor.fetchall()
        conn.close()
        return transactions
