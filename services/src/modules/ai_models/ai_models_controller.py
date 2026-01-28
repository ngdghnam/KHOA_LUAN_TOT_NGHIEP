from fastapi import APIRouter, Depends
from src.interceptors.resonse_interceptor import InterceptRoute
from src.dtos.pagination_dto import PaginationDto
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session

router = APIRouter(prefix="/ai-models", tags=["AI Models"], route_class=InterceptRoute)