from pydantic import BaseModel
from typing import Optional

class ScannedCvDto(BaseModel):
    cv_name: str
    fakeId: Optional[str] = ""