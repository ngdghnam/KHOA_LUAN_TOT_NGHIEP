import bcrypt

class UserUtil:
    def __init__(self):
        self.saltRounds = 10

    async def hashPassword(self, password: str) -> str:
        salt = bcrypt.gensalt(self.saltRounds); 
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def comparePassword(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password, hashed_password)
    
    def validate_user(self):
        return