from src.base.base_repository import BaseRepository
from src.entities.user_entity import UserEntity

class UserRepository(BaseRepository[UserEntity]): 
    def __init__(self, session=None):
        super().__init__(UserEntity, session)
        