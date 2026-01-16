
from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AISummaryResultEntity(BaseEntity):
    __tablename__ = "ai_summary_results"

    key_strengths : Mapped[str] = mapped_column(String(500), nullable=True)
    key_weaknesses : Mapped[str] = mapped_column(String(500), nullable=True)
    priority_improvements : Mapped[str] = mapped_column(String(500), nullable=True)
    career_level : Mapped[str] = mapped_column(String(100), nullable=True)
    summary_text : Mapped[str] = mapped_column(TEXT, nullable=False)
    final_score : Mapped[float] = mapped_column(nullable=True)

    # RELATIONSHIPS
    session_id: Mapped[int] = mapped_column(ForeignKey("cv_analysis_sessions.id"), nullable=False)
    session: Mapped["CvAnalysisSessionEntityEntity"] = relationship(back_populates="ai_summary_results")  # type: ignore