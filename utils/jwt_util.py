import jwt
from utils.logger import log_error

SECRET_KEY = "fastx_secret"

def generate_token(email, role):
    payload = {
        "email": email,
        "role": role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception as exception:
        log_error(f"JWT Token Read Failed: {str(exception)}")
        return None