import uuid
from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ArticleRecommendationEntity(BaseEntity):
    __tablename__ = 'article_recommendations'

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cv_analysis_sessions.id"), nullable=False)
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), nullable=False)

    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    priority : Mapped[int] = mapped_column(Integer, nullable=False)

    # RELATIONSHIPS
    session: Mapped["CvAnalysisSessionEntity"] = relationship(back_populates="article_recommendations")  # type: ignore
    article: Mapped["ArticleEntity"] = relationship(back_populates="article_recommendations")  # type: ignore
