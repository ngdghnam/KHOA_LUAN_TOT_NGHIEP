from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user_entity import UserEntity

class MediaFileEntity(BaseEntity):
    __tablename__ = "media_files"

    type: Mapped[str] = mapped_column(String(50), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # RELATIONSHIPS
    user: Mapped["UserEntity"] = relationship(back_populates="media_files")
    cv_sessions: Mapped[list["CvAnalysisSessionEntity"]] = relationship(back_populates="cv_file") # type: ignore