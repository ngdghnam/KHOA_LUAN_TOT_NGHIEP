from src.base.base_service import BaseService
from src.entities.user_entity import UserEntity
from .dtos.user_create_dto import CreateUserDto
from .dtos.user_update_dto import UpdateUserDto
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user_repository import UserRepository
from src.utils.user_util import UserUtil
from src.dtos.pagination_dto import PaginationDto
from datetime import date
from uuid import uuid4

class UserService(BaseService[UserEntity, CreateUserDto, UpdateUserDto]):
    def __init__(self, session: AsyncSession):
        repo = UserRepository(session)
        super().__init__(repo)
        self.util = UserUtil()

    async def _before_create(self, data: CreateUserDto) -> any:
        hashed_password = await self.util.hashPassword(data.password)
        transformed = {
            "id": uuid4(),
            "email": data.email,
            "username": data.username,
            "last_name": data.lastName,
            "first_name": data.firstName,
            "hashed_password": hashed_password,
            "created_at": date.today(),
            "role_id": data.roleId
        }
        return transformed
    
    async def create(self, data):
        return await super().create(data)
        
    async def _before_update(self, data: UpdateUserDto):
        transformed = {}

        if data.email is not None:
            transformed["email"] = data.email

        if data.username is not None:
            transformed["username"] = data.username

        if data.firstName is not None:
            transformed["first_name"] = data.firstName

        if data.lastName is not None:
            transformed["last_name"] = data.lastName

        if data.password is not None:
            transformed["hashed_password"] = await self.util.hashPassword(data.password)

        if data.roleId is not None:
            transformed["role_id"] = data.roleId

        transformed["updated_at"] = date.today()

        return transformed
    
    async def update(self, id, data):
        return await super().update(id, data)
    
    async def delete(self, id):
        return await super().delete(id)
    
    async def findOne(self, data: str):
        where = {
            "id": data
        }
        return await super().findOne({
            "where": where,
            "select": ["id", "username", "email", "first_name", "last_name"]
        })
    
    async def find(self, options):
        return await super().find(options)
    
    async def updateActive(self, id: str):
        data = await self.baseRepo.findOne({
            "where": {
                "id": id
            }
        })

        is_deleted = not data.is_deleted
        return await self.baseRepo.update(data.id, {
            "is_deleted": is_deleted,
            "created_at": date.today()
        })
    
    async def findAll(self):
        return await super().findAll()
    
    async def pagination(data: PaginationDto):
        return
    
