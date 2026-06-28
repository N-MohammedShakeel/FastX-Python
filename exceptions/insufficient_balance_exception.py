class InsufficientBalanceException(Exception):
    def __init__(self, message="Insufficient balance"):
        super().__init__(message)