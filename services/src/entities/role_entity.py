from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class RoleEntity(BaseEntity):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(100))
    users: Mapped[list["UserEntity"]] = relationship(back_populates="role") # type: ignore