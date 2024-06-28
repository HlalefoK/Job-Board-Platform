import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('db/finance_tracker.db')
cursor = conn.cursor()

# Drop existing tables if needed (for reinitialization)
cursor.execute('DROP TABLE IF EXISTS User')
cursor.execute('DROP TABLE IF EXISTS "Transaction"')

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

print("Database initialized.")
