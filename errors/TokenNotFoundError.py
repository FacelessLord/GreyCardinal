
class TokenNotFoundError(Exception):
    def __init__(self):
        self.message = "Token not found. Shutting down"
