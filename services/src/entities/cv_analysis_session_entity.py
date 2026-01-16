import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import CheckConstraint, DateTime, Index, String, Index, UUID, DateTime, Boolean, ForeignKey, Text, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CvAnalysisSessionEntity(BaseEntity):
    __tablename__ = "cv_analysis_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    cv_file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("media_files.id"), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    overall_score: Mapped[float | None] = mapped_column(DECIMAL(5, 2))
    error_message: Mapped[str | None] = mapped_column(Text)
    processing_time: Mapped[int | None] = mapped_column(Integer)
    analysis_type: Mapped[str | None] = mapped_column(String(50))
    completed_at: Mapped[DateTime | None] = mapped_column(DateTime)

    __table_args__ = (
        CheckConstraint("overall_score >= 0 AND overall_score <= 100"),
        CheckConstraint("status IN ('PENDING','PROCESSING','DONE','FAILED')"),
        Index("idx_sessions_user_status", "user_id", "status"),
    )

    user: Mapped["UserEntity"] = relationship(back_populates="cv_sessions") # type: ignore    
    cv_file: Mapped["MediaFileEntity"] = relationship(back_populates="cv_sessions") # type: ignore

    ai_results: Mapped[list["AiAnalysisResultEntity"]] = relationship(back_populates="session") # type: ignore
    summary: Mapped["AISummaryResultEntity"] = relationship(back_populates="session", uselist=False) # type: ignore
    missing_skills: Mapped[list["SessionMissingSkill"]] = relationship(back_populates="session") # type: ignore
    course_recommendations: Mapped[list["CourseRecommendation"]] = relationship(back_populates="session")  # type: ignore
    article_recommendations: Mapped[list["ArticleRecommendationEntity"]] = relationship(back_populates="session") # type: ignore
    feedbacks: Mapped[list["UserSessionFeedbackEntity"]] = relationship(back_populates="session") # type: ignore
