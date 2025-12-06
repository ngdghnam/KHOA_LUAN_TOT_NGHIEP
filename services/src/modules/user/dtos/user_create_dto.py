from pydantic import BaseModel

class CreateUserDto(BaseModel):
    email: str
    username: str 
    lastName: str 
    firstName: str 
    password: str