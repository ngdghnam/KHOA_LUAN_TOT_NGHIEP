from base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean

class UserEntity(BaseEntity): 
    __tablename__ = "users"
    email = Column(String(100))
    password = Column(String(255))
    lastName = Column(String(100))
    firstName = Column(String(100))
    phoneNumber = Column(String(100))
    address = Column(String(100))