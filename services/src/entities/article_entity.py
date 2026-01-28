from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ArticleEntity(BaseEntity):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    author: Mapped[str] = mapped_column(String(100), nullable=True)
    published_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    # RELATIONSHIPS
    skills: Mapped[list["ArticleSkillEntity"]] = relationship(back_populates="article")  # type: ignore  ✅ Changed from "article_skills"
    tags: Mapped[list["ArticleTagMappingEntity"]] = relationship(back_populates="article")  # type: ignore
    recommendations: Mapped[list["ArticleRecommendationEntity"]] = relationship(back_populates="article") # type: ignore