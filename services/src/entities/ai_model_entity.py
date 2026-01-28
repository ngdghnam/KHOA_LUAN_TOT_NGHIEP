
from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AIModelEntity(BaseEntity):
    __tablename__ = 'ai_models'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(100))
    version: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
