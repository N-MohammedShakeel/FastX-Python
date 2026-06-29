from functools import wraps
import sys

def check_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        main = sys.modules["__main__"]
        if not main.CURRENT_USER:
            print("\nAuthentication Error: Action blocked. No session found. Please login.")
            return None
        return func(*args, **kwargs)
    return wrapper

def role_allowed(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            main = sys.modules["__main__"]
            if not main.CURRENT_USER or main.CURRENT_USER.role not in roles:
                print(f"\nAuthorization Error: Access denied. Requires {roles} role.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator