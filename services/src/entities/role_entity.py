from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user_entity import UserEntity

class RoleEntity(BaseEntity):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    users: Mapped[list["UserEntity"]] = relationship(back_populates="role") # type: ignore