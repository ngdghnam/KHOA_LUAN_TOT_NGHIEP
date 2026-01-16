from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Index, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SkillEntity(BaseEntity):
    __tablename__ = "skills"

    __table_args__ = (
        Index('idx_skills_category', 'category'),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (
        Index('idx_skills_category', 'category'),
    )

    # RELATIONSHIPS
    session_missing_skills: Mapped[list["SessionMissingSkillEntity"]] = relationship(back_populates="skill")  # type: ignore
    articles_skills: Mapped[list["ArticleSkillEntity"]] = relationship(back_populates="skill")  # type: ignore