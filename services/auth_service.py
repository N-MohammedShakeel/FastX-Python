import json, os
from repositories.user_repository import UserRepository
from exceptions.invalid_credentials_exception import InvalidCredentialsException
from models.user import User
from utils.logger import log_info, log_warning, log_error
from utils.password_util import hash_password, verify_password
from utils.jwt_util import generate_token, decode_token

SESSION_FILE = "session.json"

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, name, email, password, role):
        
        if self.user_repo.find_by_email(email):
            log_warning(f"Registration failed. Email already exists: {email}")
            return False
        
        hashed_password = hash_password(password)
        new_user = User(None, name, email, hashed_password, role, 0.00)
        status = self.user_repo.save(new_user)

        if status:
            log_info(f"{role} registered successfully. Email: {email}")
        else:
            log_error(f"Registration failed for {email}")

        return status

    def login(self, email, password):
        user = self.user_repo.find_by_email(email)
        if user and verify_password(password, user.password):
            token = generate_token(user.email, user.role)
            with open(SESSION_FILE, "w") as file:
                json.dump({"token": token}, file)
            log_info(f"Login successful. User: {email}, Role: {user.role}")
            return user
        else:
            log_warning(f"Invalid login attempt: {email}")
            raise InvalidCredentialsException()

    def get_auto_session(self):
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
            log_info(f"Auto login payload found: {payload['email']}")
            return self.user_repo.find_by_email(payload["email"])
        except Exception as exception:
            log_error(f"Auto session failed: {exception}")
            return None

    def logout(self, email):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "w") as file:
                json.dump({}, file)
            log_info(f"User logged out. Email: {email}")