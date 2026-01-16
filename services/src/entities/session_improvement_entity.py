from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user_entity import UserEntity
from .cv_analysis_session_entity import CvAnalysisSessionEntityEntity


class SessionImprovementEntity(BaseEntity):
    __tablename__ = "session_improvements"

    improvement_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    implemented_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    score_change: Mapped[float] = mapped_column(Integer, nullable=False)
    improvements: Mapped[str] = mapped_column(String(1000), nullable=True)
    old_session_id: Mapped[UUID] = mapped_column(UUID, nullable=False), ForeignKey("cv_analysis_sessions.id")
    new_session_id: Mapped[UUID] = mapped_column(UUID, nullable=False), ForeignKey("cv_analysis_sessions.id")

    # RELATIONSHIPS
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserEntity"] = relationship(back_populates="session_improvements")  # type: ignore
    