# auth.py
import json
import os
import bcrypt

USERS_FILE = "users.json"


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def register_user(email, password):
    """Register a new normal user."""
    users = _load_users()
    if email in users:
        return False, "User already exists."

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"password": hashed_pw, "role": "user", "usage": 0}
    _save_users(users)
    return True, "User registered successfully."


def authenticate_user(email, password):
    """Authenticate both admin and normal users."""
    # Fixed Admin credentials
    if email.lower() == "admin" and password == "Poiu1234@@":
        return True, "admin"

    users = _load_users()
    if email not in users:
        return False, None
    hashed_pw = users[email]["password"]
    if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
        return True, users[email]["role"]
    return False, None


def increment_usage(email):
    """Increment usage count for a user."""
    users = _load_users()
    if email in users:
        users[email]["usage"] = users[email].get("usage", 0) + 1
        _save_users(users)


def get_all_users():
    """Return all registered users with their usage count."""
    users = _load_users()
    return [
        {"email": u, "role": users[u]["role"], "usage": users[u].get("usage", 0)}
        for u in users
    ]
