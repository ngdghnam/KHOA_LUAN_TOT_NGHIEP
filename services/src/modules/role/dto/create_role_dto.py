from pydantic import BaseModel
from typing import Optional

class CreateRoleDto(BaseModel):
    roleName: str