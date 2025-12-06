from fastapi.routing import APIRoute
from fastapi import Request, Response
from src.dtos.response_dto import ResponseDto
from src.config.serialize import serialize
from fastapi.responses import JSONResponse

class InterceptRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            result = await original_handler(request)

            # Nếu đã là Response object (JSONResponse, StreamingResponse, etc.)
            # thì return luôn, KHÔNG wrap thêm
            if isinstance(result, Response):
                return result

            # Wrap data thường vào ResponseDto
            response = ResponseDto(
                success=True,
                message="OK",
                data=serialize(result)
            )

            return JSONResponse(
                status_code=200,
                content=response.model_dump()
            )

        return custom_handler