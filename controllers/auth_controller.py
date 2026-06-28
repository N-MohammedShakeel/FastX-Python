from services.auth_service import AuthService
from validators.validators import is_valid_email, is_valid_password
from exceptions.invalid_credentials_exception import InvalidCredentialsException

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def register_passenger(self, name, email, password):
        if not is_valid_email(email) or not is_valid_password(password):
            return False
        if self.auth_service.register(name, email, password, 'PASSENGER'):
            print("\nSUCCESS: Passenger Registration Successful. Proceed to login.")
            return True
        print("ERROR: Registration Failed.")
        return False

    def register_operator(self, name, email, password):
        if not is_valid_email(email) or not is_valid_password(password):
            return False
        if self.auth_service.register(name, email, password, 'OPERATOR'):
            print("SUCCESS: Operator Registration Successful. Proceed to login.")
            return True
        print("ERROR: Registration Failed.")
        return False

    def login(self, email, password):
        
        user = None
        try:
            user = self.auth_service.login(email, password)
        except InvalidCredentialsException as exception:
            print("\nERROR: Login Failed.", exception)

        if user:
            print(f"\nSUCCESS: Login Successful! Welcome, {user.name}.")
            return user
        
        return None
    
    def get_auto_session(self):
        return self.auth_service.get_auto_session()

    def logout(self, email):
        self.auth_service.logout(email)