from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseDto(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None

    model_config = {
        "arbitrary_types_allowed": True  
    }
