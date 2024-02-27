from pathlib import Path
from db import DB
from encode import hash
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Save the hashed passwords to the db
db = DB()

tokens = [generate_random_string(10) for _ in range(100)]
hashes = [hash(token) for token in tokens]

#create a csv file with the tokens and their hashes
with open("tokens.csv", "w") as f:
    for token, hash in zip(tokens, hashes):
        f.write(f"{token},{hash}\n")

for token in enumerate(tokens):
    db.save_tokenHash(hashes[token[0]])
    print(f"Token: {token[1]}, Hash: {hashes[token[0]]} saved to the database.")

db.__del__()