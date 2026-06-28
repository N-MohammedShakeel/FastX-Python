import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$"
    is_valid = bool(re.match(pattern, email))
    if not is_valid:
        print("ERROR: Invalid Email")
    return is_valid

def is_valid_password(password):
    if len(password) < 6:
        print("ERROR: Password is invalid. Min password length is 6.")
    return len(password) >= 6