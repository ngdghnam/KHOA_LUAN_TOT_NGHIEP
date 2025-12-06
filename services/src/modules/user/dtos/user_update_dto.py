from typing import Optional
from pydantic import BaseModel

class UpdateUserDto(BaseModel):
    email: Optional[str]
    username: Optional[str]
    lastName: Optional[str]
    firstName: Optional[str]
    password: Optional[str]