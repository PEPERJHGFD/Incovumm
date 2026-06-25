from config import AUTH_USER

class AuthController:
    def login(self, username: str, password: str) -> bool:
        return username == AUTH_USER["username"] and password == AUTH_USER["password"]
