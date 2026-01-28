import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import CheckConstraint, Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SessionKeywordEntity(BaseEntity):
    __tablename__ = "session_keywords"

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cv_analysis_sessions.id"), nullable=False
    )

    session: Mapped["CvAnalysisSessionEntity"] = relationship(back_populates="keywords")  # type: ignore