class UserNotFoundException(Exception):
    def __init__(self, message="Requested user not found"):
        super().__init__(message)