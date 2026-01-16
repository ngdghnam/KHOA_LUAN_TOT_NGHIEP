from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AnalysisStrengthEntity(BaseEntity):
    __tablename__ = "analysis_strengths"

    __table_args__ = (
        Index('idx_analysis_strengths_type', 'strength_type'),
    )

    strength_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    category : Mapped[str] = mapped_column(String(50), nullable=False)
    priority : Mapped[int] = mapped_column(Integer, nullable=False)

    # RELATIONSHIPS
    analysis_id : Mapped[int] = mapped_column(ForeignKey("ai_analysis_results.id"), nullable=False)
    analysis: Mapped["AiAnalysisResultEntity"] = relationship(back_populates="strengths")  # type: ignore
