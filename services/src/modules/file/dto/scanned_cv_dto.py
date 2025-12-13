from pydantic import BaseModel

class ScannedCvDto(BaseModel):
    cv_name: str