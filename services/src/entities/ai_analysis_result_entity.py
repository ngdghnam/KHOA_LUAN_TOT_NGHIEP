from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class AiAnalysisResultEntity(BaseEntity):
    __tablename__ = "ai_analysis_results"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cv_analysis_sessions.id"),
        nullable=False
    )

    ai_model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_models.id"),
        nullable=False
    )

    result_data: Mapped[str] = mapped_column(String(1000), nullable=False)
    confidence_score: Mapped[float] = mapped_column(nullable=False)
    analyzed_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    raw_response: Mapped[str | None] = mapped_column(String(2000))

    __table_args__ = (
        Index('idx_analysis_session', 'session_id'),
        Index('idx_analysis_model', 'ai_model_id'),
    )

    # RELATIONSHIPS
    session: Mapped["CvAnalysisSessionEntityEntity"] = relationship(
        back_populates="ai_results"
    ) # type: ignore

    ai_model: Mapped["AIModelEntity"] = relationship(
        back_populates="ai_analysis_results"
    ) # type: ignore

    strengths: Mapped[list["AnalysisStrengthEntity"]] = relationship(back_populates="analysis") # type: ignore
    weaknesses: Mapped[list["AnalysisWeaknessEntity"]] = relationship(back_populates="analysis") # type: ignore
    format_issues: Mapped[list["AnalysisFormatIssueEntity"]] = relationship(back_populates="analysis") # type: ignore

