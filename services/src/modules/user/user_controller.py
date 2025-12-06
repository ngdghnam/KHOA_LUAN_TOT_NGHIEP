from fastapi import APIRouter, Depends
from .user_service import UserService
from .dtos.user_create_dto import CreateUserDto
from .dtos.user_update_dto import UpdateUserDto

from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session
from src.constants.index import CREATE_SUCCESS, UPDATE_SUCCESS, GET_ALL_SUCCESS, DELETE_SUCCESS
from src.dtos.pagination_dto import PaginationDto
from src.dtos.response_dto import ResponseDto
from src.interceptors.resonse_interceptor import InterceptRoute

router = APIRouter(prefix="/users", tags=["users"], route_class=InterceptRoute)

@router.post("/create")
async def create(data: CreateUserDto, session: AsyncSession = Depends(get_session)):
    service: UserService = UserService(session)
    return await service.create(data)

@router.put("/update/{id}")
async def update(id: str, data: UpdateUserDto, session: AsyncSession = Depends(get_session)):
    service: UserService = UserService(session)
    return await service.update(id, data)

@router.get("")
async def getAllUsers(session: AsyncSession = Depends(get_session)):
    service: UserService = UserService(session)
    return await service.findAll()

@router.delete("/delete/{id}")
async def update_active(id: str, session: AsyncSession = Depends(get_session)):
    service: UserService = UserService(session)
    return await service.updateActive(id)
   
@router.get("/pagination")
async def pagination(data: PaginationDto, session: AsyncSession = Depends(get_session)):
    service: UserService = UserService(session)
    return