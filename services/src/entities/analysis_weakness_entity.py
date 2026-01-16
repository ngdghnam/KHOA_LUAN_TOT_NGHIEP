from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AnalysisWeaknessEntity(BaseEntity):
    __tablename__ = "analysis_weaknesses"

    __table_args__ = (
        Index('idx_analysis_weaknesses_type', 'weakness_type'),
    )

    weakness_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)

    # RELATIONSHIPS
    analysis_id : Mapped[int] = mapped_column(ForeignKey("ai_analysis_results.id"), nullable=False)
    analysis: Mapped["AiAnalysisResultEntity"] = relationship(back_populates="weaknesses")  # type: ignore