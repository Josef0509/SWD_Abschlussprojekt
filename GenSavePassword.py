from pathlib import Path
from db import DB
from encode import hash


def save_credentials(username, password):
    db = DB()
    hashed_password = hash(password)
    db.save_credentials(username, hashed_password)
    print(f"Saved {username} with password {hashed_password}")
    db.__del__()

