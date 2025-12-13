from pydantic import BaseModel

class RegisterUserDto(BaseModel):
    username: str 
    password: str