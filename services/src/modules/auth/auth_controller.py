from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session
from src.constants.index import CREATE_SUCCESS, UPDATE_SUCCESS, GET_ALL_SUCCESS, DELETE_SUCCESS
from src.interceptors.resonse_interceptor import InterceptRoute
from .dto.register_user_dto import RegisterUserDto
from .dto.login_dto import LoginDto
from src.dtos.user_dto import UserDto

router = APIRouter(prefix="/auth", tags=["auth"], route_class=InterceptRoute)

@router.post("/register")
async def register(data: RegisterUserDto):
    return

@router.post("/login")
async def login(data: LoginDto):
    return

@router.post("/logout")
async def logout():
    return

@router.post("/current_user")
async def get_current_user(user: UserDto):
    return user