from abc import ABC, abstractmethod

class BaseService(ABC): 
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def post(): 
        pass

    @abstractmethod
    async def get():
        pass

    @abstractmethod
    async def put():
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

