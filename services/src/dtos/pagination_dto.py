from pydantic import BaseModel

class PaginationDto(BaseModel): 
    where: dict
    skip: int
    take: int