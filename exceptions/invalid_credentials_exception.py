class InvalidCredentialsException(Exception):
    def __init__(self, message="Provided Credentials are invalid"):
        super().__init__(message)