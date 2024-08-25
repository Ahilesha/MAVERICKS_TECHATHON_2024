import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return True
    else:
        return False

# Example usage
if verify_user('example_user', 'example_password'):
    print("Login successful!")
else:
    print("Invalid username or password.")
