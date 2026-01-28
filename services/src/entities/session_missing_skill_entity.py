
import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import CheckConstraint, Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SessionMissingSkillEntity(BaseEntity):
    __tablename__ = "session_missing_skills"

    __table_args__ = (
        CheckConstraint("importance >= 1 AND importance <= 5", name="check_importance_range"),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cv_analysis_sessions.id"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id"), nullable=False
    )

    importance: Mapped[str] = mapped_column(String(50), nullable=False)
    detected_level: Mapped[str | None] = mapped_column(String(50))
    required_level: Mapped[str | None] = mapped_column(String(50))
    gap_analysis: Mapped[str | None] = mapped_column(Text)

    # RELATIONSHIPS
    session: Mapped["CvAnalysisSessionEntity"] = relationship(back_populates="missing_skills")  # type: ignore
    skill: Mapped["SkillEntity"] = relationship(back_populates="session_missing_skills")  # type: ignore