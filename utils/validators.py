import re

def is_valid_email(email):
    """Checks string properties using regular expression matching."""
    pattern = r"^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_valid_password(password):
    """Enforces basic baseline character length validations."""
    return len(password) >= 6