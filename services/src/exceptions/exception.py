from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.dtos.response_dto import ResponseDto

async def custom_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseDto(
            status=exc.status_code,
            message=exc.detail,
            data=None
        ).model_dump()
    )