import hashlib

def hash(password: str) -> str:
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Update the hash object with the password bytes
    sha256_hash.update(password_bytes)

    # Get the hexadecimal representation of the hashed password
    hashed_password = sha256_hash.hexdigest()
    return hashed_password
