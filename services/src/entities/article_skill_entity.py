from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class ArticleSkillEntity(BaseEntity):
    __tablename__ = "article_skills"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency_level: Mapped[str] = mapped_column(String(50), nullable=False)

    # RELATIONSHIPS
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), nullable=False)
    article: Mapped["ArticleEntity"] = relationship(back_populates="skills")  # ✅ Changed

    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), nullable=False)
    skill: Mapped["SkillEntity"] = relationship(back_populates="articles_skills")  # ✅ Changed