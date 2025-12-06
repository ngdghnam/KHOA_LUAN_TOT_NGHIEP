from typing import Optional
from pydantic import BaseModel

class UpdateUserDto(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    password: Optional[str] = None
    roleId: Optional[str] = None
