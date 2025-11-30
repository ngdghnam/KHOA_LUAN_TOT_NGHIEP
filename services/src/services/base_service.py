from abc import ABC, abstractmethod

class BaseService(ABC): 
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def create(): 
        pass

    @abstractmethod
    async def find():
        pass

    @abstractmethod
    async def findOne():
        pass

    @abstractmethod
    async def findAll():
        pass

    @abstractmethod
    async def update():
        pass

    @abstractmethod
    async def delete():
        pass 

    @abstractmethod
    async def updateActive():
        pass

    @abstractmethod
    async def loadSelectionBox():
        pass

