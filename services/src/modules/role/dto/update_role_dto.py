from pydantic import BaseModel
from typing import Optional

class UpdateRoleDto(BaseModel):
    roleName: Optional[str] = None