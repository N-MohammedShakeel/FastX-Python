import json
import os
from utils.db import get_connection
from utils.password_util import hash_password, verify_password
from utils.jwt_util import generate_token, decode_token
from utils.logger import log_info, log_warning, log_error

SESSION_FILE = "session.json"

class AuthService:
    def register(self, name, email, password, role):
        """Creates a new record entry in the users table."""
        conn = get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            hashed = hash_password(password)
            
            query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, hashed, role))
            conn.commit()
            
            log_info(f"User Registered: {email} as {role}")
            return True
        except Exception as exception:
            log_error(f"Registration Query Crashed: {exception}")
            return False
        finally:
            conn.close()

    def login(self, email, password):
        """Verifies account credentials and builds the active session tracking state."""
        conn = get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            if user and verify_password(password, user["password"]):
                token = generate_token(user["email"], user["role"])
                
                with open(SESSION_FILE, "w") as file:
                    json.dump({"token": token}, file)
                
                log_info(f"User Logged In: {email}")
                return user
            
            log_warning(f"Invalid Login Attempt for: {email}")
            return None
        except Exception as exception:
            log_error(f"Login Verification Failure: {exception}")
            return None
        finally:
            conn.close()

    def get_auto_session(self):
        """Reads local JSON parameters to re-instantiate active context loops."""
        if not os.path.exists(SESSION_FILE):
            return None
            
        try:
            with open(SESSION_FILE, "r") as file:
                data = json.load(file)
            
            token = data.get("token")
            if not token:
                return None
                
            payload = decode_token(token)
            if not payload:
                return None
                
            conn = get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (payload["email"],))
            user = cursor.fetchone()
            return user
        except Exception:
            return None

    def logout(self):
        """Flushes token values from the text storage file."""
        try:
            if os.path.exists(SESSION_FILE):
                with open(SESSION_FILE, "w") as file:
                    json.dump({}, file)
            log_info("User Logged Out")
            return True
        except Exception as exception:
            log_error(f"Logout Failure: {exception}")
            return
