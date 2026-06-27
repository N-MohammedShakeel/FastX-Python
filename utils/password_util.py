import bcrypt

def hash_password(password):
    """Converts a plaintext string to an encrypted secure string token."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Checks the password against the stored database value."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False