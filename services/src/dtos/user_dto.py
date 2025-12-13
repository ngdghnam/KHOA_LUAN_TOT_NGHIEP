
from pydantic import BaseModel

class UserDto(BaseModel):
    username: str
    email: str 
    roleId: str
    roleName: str
    accessToken: str