import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import CheckConstraint, DateTime, Index, String, Index, UUID, DateTime, Boolean, ForeignKey, Text, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CvAnalysisSessionEntity(BaseEntity):
    __tablename__ = "cv_analysis_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    cv_file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("media_files.id"), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    completed_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("overall_score >= 0 AND overall_score <= 100"),
        CheckConstraint("status IN ('PENDING','PROCESSING','DONE','FAILED')"),
        Index("idx_sessions_user_status", "user_id", "status"),
    )

    user: Mapped["UserEntity"] = relationship(back_populates="cv_sessions") # type: ignore    
    cv_file: Mapped["MediaFileEntity"] = relationship(back_populates="cv_sessions") # type: ignore

    ai_summary_results: Mapped["AISummaryResultEntity"] = relationship(back_populates="session", uselist=False) # type: ignore
    missing_skills: Mapped[list["SessionMissingSkillEntity"]] = relationship(back_populates="session") # type: ignore
    article_recommendations: Mapped[list["ArticleRecommendationEntity"]] = relationship(back_populates="session") # type: ignore

    questions: Mapped[list["QuestionEntity"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    skill_gaps: Mapped[list["SessionSkillGapEntity"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    keywords: Mapped[list["SessionKeywordEntity"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # course_recommendations: Mapped[list["CourseRecommendation"]] = relationship(back_populates="session")  # type: ignore
    # feedbacks: Mapped[list["UserSessionFeedbackEntity"]] = relationship(back_populates="session") # type: ignore
