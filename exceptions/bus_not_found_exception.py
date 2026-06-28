class BusNotFoundException(Exception):
    def __init__(self, message="Requested bus not found"):
        super().__init__(message)