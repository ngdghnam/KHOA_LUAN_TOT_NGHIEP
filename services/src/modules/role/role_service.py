from src.base.base_service import BaseService
from src.entities.role_entity import RoleEntity
from .dto.create_role_dto import CreateRoleDto
from .dto.update_role_dto import UpdateRoleDto
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.role_repository import RoleRepository
import uuid
from datetime import date
from typing import Optional, Dict, Any

class RoleService(BaseService[RoleEntity, CreateRoleDto, UpdateRoleDto]):
    def __init__(self, session: AsyncSession):
        repo = RoleRepository(session)
        super().__init__(repo)

    async def _before_create(self, data: CreateRoleDto):
        transformed = {
            "id": uuid.uuid4(),
            "name": data.roleName,
            "created_at": date.today(),
        }
        return transformed
    
    async def _before_update(self, data):
        transformed = {
            "name": data.roleName,
            "updated_at": date.today(),
        }
        return transformed
    
    async def create(self, data):

        check = await self.findOne({
            "where": {
                "name": data.roleName
            }
        })

        if (check): raise ValueError("Duplicate data")

        return await super().create(data)
    
    async def update(self, id, data):
        check = await self.findOne({
            "where": {
                "id": id
            }
        })
        if (not check): raise ValueError("Data not found")

        return await super().update(id, data)
    
    async def findAll(self, options: Optional[Dict[str, Any]] = None):
        return await super().findAll({
            "relations": ["users"]
        })

    async def delete(self, id):
        return await super().delete(id)
    
    async def findOne(self, data: str):
        return await super().findOne({
            "where": {
                "id": data,
            }
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