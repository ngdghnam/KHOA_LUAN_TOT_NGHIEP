from pydantic import BaseModel

class SearchDto(BaseModel):
    query: str
