class InsufficientSeatsException(Exception):
    def __init__(self, message="Insufficient seats available"):
        super().__init__(message)