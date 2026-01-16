from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AnalysisFormatIssueEntity(BaseEntity):
    __tablename__ = "analysis_format_issues"

    issue_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    location : Mapped[str] = mapped_column(String(100), nullable=True)

    # RELATIONSHIPS
    analysis_id : Mapped[int] = mapped_column(ForeignKey("ai_analysis_results.id"), nullable=False)
    analysis: Mapped["AiAnalysisResultEntity"] = relationship(back_populates="format_issues")  # type: ignore