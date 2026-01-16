import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AiModelPerformanceEntity(BaseEntity):
    __tablename__ = 'ai_model_performance'

    avg_score: Mapped[float] = mapped_column(nullable=False)
    total_analyses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_processing_time: Mapped[float] = mapped_column(nullable=False)
    sucess_rate: Mapped[float] = mapped_column(nullable=False)

    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_models.id"), nullable=False)
    model: Mapped["AIModelEntity"] = relationship(back_populates="performances")  # type: ignore
