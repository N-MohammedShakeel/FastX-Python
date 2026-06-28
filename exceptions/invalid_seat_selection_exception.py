class InvalidSeatSelectionException(Exception):
    def __init__(self, message="Selected Seats are not available"):
        super().__init__(message)