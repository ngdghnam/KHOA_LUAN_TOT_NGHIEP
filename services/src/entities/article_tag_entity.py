
from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .article_entity import ArticleEntity
from .article_tag_mapping_entity import ArticleTagMappingEntity

class ArticleTagEntity(BaseEntity):
    __tablename__ = "article_tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    articles: Mapped[list["ArticleTagMappingEntity"]] = relationship(back_populates="tag")
