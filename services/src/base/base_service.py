from abc import ABC, abstractmethod
from .base_repository import BaseRepository
from typing import TypeVar, Generic
from .options import *

T = TypeVar('T')
CreateDto = TypeVar('CreateDto')
UpdateDto = TypeVar('UpdateDto')

class BaseService(ABC, Generic[T, CreateDto, UpdateDto]): 
    def __init__(self, baseRepo: BaseRepository[T]) -> None:
        self.baseRepo = baseRepo

    async def _before_create(self, data: CreateDto) -> CreateDto:
        return data

    async def _before_update(self, data: UpdateDto) -> UpdateDto:
        return data

    @abstractmethod
    async def create(self, data: CreateDto) -> T:
        data =  await self._before_create(data) 
        return await self.baseRepo.create(data)

    @abstractmethod
    async def find(self, options: FindOptions):
        return await self.baseRepo.find(options)

    @abstractmethod
    async def findOne(self, data: Dict) -> T:
        return await self.baseRepo.findOne(data)

    @abstractmethod
    async def findAll(self, options: Optional[Dict[str, Any]] = None):
        return await self.baseRepo.find(options)

    @abstractmethod
    async def update(self, id: str, data: UpdateDto) -> T:
        data = await self._before_update(data)
        return await self.baseRepo.update(id, data)

    @abstractmethod
    async def delete(self, id: str) -> bool:
        return await self.baseRepo.delete(id)

