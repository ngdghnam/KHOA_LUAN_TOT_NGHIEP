from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class UserEntity(BaseEntity):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(150))
    last_name: Mapped[str | None] = mapped_column(String(150))
    hashed_password: Mapped[str | None] = mapped_column(String(255))

    role_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("roles.id"))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[DateTime | None] = mapped_column(DateTime)

    role: Mapped["Role"] = relationship(back_populates="users") # type: ignore
    media_files: Mapped[list["MediaFileEntity"]] = relationship(back_populates="user", foreign_keys="MediaFileEntity.user_id") # type: ignore
    cv_sessions: Mapped[list["CvAnalysisSessionEntityEntity"]] = relationship(back_populates="user") # type: ignore