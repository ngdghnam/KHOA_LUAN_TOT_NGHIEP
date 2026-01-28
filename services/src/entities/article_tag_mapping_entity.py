from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class ArticleTagMappingEntity(BaseEntity):
    __tablename__ = "article_tag_mappings"

    tag_name: Mapped[str] = mapped_column(ForeignKey("article_tags.name"), nullable=False)  # ✅ Add ForeignKey
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), nullable=False)

    # RELATIONSHIPS
    article: Mapped["ArticleEntity"] = relationship(back_populates="tags")  # type: ignore
    tag: Mapped["ArticleTagEntity"] = relationship(back_populates="articles") # type: ignore