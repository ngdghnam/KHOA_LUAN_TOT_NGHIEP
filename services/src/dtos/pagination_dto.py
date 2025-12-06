from pydantic import BaseModel
from typing import Optional

class PaginationDto(BaseModel): 
    where: Optional[dict] = {}
    skip: Optional[int] = 0 
    take: Optional[int] = 10