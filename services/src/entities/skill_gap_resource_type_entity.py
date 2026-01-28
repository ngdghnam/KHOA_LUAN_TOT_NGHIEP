from src.entities.base_entity import BaseEntity
from sqlalchemy import Column, Index, Integer, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class SkillGapResourceTypeEntity(BaseEntity):
    __tablename__ = "skill_gap_resource_types"

    skill_gap_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("session_skill_gaps.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)

    skill_gap: Mapped["SessionSkillGapEntity"] = relationship(
        back_populates="resource_types"
    ) # type: ignore
