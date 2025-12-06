from services.src.base.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class RoleEntity(BaseEntity):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(100))