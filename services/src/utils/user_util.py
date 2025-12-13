import bcrypt
from typing import TYPE_CHECKING

# Only import for type checking, not at runtime
if TYPE_CHECKING:
    from src.modules.user.user_service import UserService
    from src.modules.auth.dto.login_dto import LoginDto

class UserUtil:
    def __init__(self):
        self.saltRounds = 10

    async def hashPassword(self, password: str) -> str:
        salt = bcrypt.gensalt(self.saltRounds)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def comparePassword(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    
    def validate_user(self, service: "UserService", data: "LoginDto"):
        # Your validation logic here
        return