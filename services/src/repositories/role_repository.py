from src.base.base_repository import BaseRepository
from src.entities.role_entity import RoleEntity
class RoleRepository(BaseRepository[RoleEntity]): 
    def __init__(self, session=None):
        super().__init__(RoleEntity, session)