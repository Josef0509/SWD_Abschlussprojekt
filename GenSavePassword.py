from pathlib import Path
from db import DB
from encode import hash


usernames = ["sstr"]
passwords = ["sa"]  #make sure to get rid of the actual password after running this script


# Save the hashed passwords to the db
db = DB()
for username, password in zip(usernames, passwords):
    hashed_password = hash(password)
    db.save_credentials(username, hashed_password)
    print(f"Saved {username} with password {hashed_password}")

db.__del__()