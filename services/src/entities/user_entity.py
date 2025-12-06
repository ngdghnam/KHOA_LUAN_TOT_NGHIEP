from services.src.base.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class UserEntity(BaseEntity): 
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_cv: Mapped[str] = mapped_column(String(255), nullable=True)