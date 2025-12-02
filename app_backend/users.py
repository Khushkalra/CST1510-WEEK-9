import hashlib
from app_backend.db import get_connection

def hash_password(password: str) -> str:
    #return a hash of the password
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(username: str, password: str):
    #register a new user if the username does not already exist
    conn = get_connection()
    cur = conn.cursor()

    try:
        #check if user already exists
        cur.execute("SELECT username FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row is not None:
            return False, "Username already exists."

        password_hash = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, "user"),
        )
        conn.commit()
        return True, "User registered successfully."
    except Exception as e:
        return False, f"Error during registration: {e}"
    finally:
        conn.close()

def login_user(username: str, password: str):
    #validate username/password combination
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        if row is None:
            return False, "User not found."

        password_hash = hash_password(password)
        if row[0] == password_hash:
            return True, "Login successful."
        else:
            return False, "Incorrect password."
    except Exception as e:
        return False, f"Error during login: {e}"
    finally:
        conn.close()