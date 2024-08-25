import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def store_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    
    try:
        cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Username already exists.")
    
    conn.close()

# Example usage
store_user('example_user', 'example_password')
