from fastapi import APIRouter, Depends
from .role_service import RoleService
from .dto.create_role_dto import CreateRoleDto
from .dto.update_role_dto import UpdateRoleDto

from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session
from src.constants.index import CREATE_SUCCESS, UPDATE_SUCCESS, GET_ALL_SUCCESS, DELETE_SUCCESS
from src.dtos.pagination_dto import PaginationDto
from src.dtos.response_dto import ResponseDto
from src.interceptors.resonse_interceptor import InterceptRoute

router = APIRouter(prefix="/roles", tags=["roles"], route_class=InterceptRoute)

@router.post("/create")
async def create(data: CreateRoleDto, session: AsyncSession = Depends(get_session)):
    service: RoleService = RoleService(session)
    return await service.create(data)

@router.put("/update/{id}")
async def update(id: str, data: UpdateRoleDto, session: AsyncSession = Depends(get_session)):
    service: RoleService = RoleService(session)
    return await service.update(id, data)

@router.get("")
async def getAllUsers(session: AsyncSession = Depends(get_session)):
    service: RoleService = RoleService(session)
    return await service.findAll()

@router.get("/detail/{id}")
async def findOne(id: str, session: AsyncSession = Depends(get_session)):
    service: RoleService = RoleService(session)
    return await service.findOne(id)

@router.delete("/delete/{id}")
async def update_active(id: str, session: AsyncSession = Depends(get_session)):
    service: RoleService = RoleService(session)
    return await service.updateActive(id)