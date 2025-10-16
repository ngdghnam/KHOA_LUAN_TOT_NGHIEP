from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self) -> None:
        pass
        
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def findOne(self):
        pass

    @abstractmethod
    def findAndCount(self):
        pass
    
    @abstractmethod
    def find(self): 
        pass

    @abstractmethod
    def save(self):
        pass