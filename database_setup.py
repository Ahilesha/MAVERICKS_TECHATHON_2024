import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for storing user login details
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
