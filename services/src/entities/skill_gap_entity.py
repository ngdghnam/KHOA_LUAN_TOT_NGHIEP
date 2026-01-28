import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.base_entity import BaseEntity

class SessionSkillGapEntity(BaseEntity):
    __tablename__ = "session_skill_gaps"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cv_analysis_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    learning_keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    skill_gap: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[str] = mapped_column(Text, nullable=False)

    # List[str] → normalize thành bảng con
    resource_types: Mapped[list["SkillGapResourceTypeEntity"]] = relationship(
        back_populates="skill_gap",
        cascade="all, delete-orphan"
    ) # type: ignore 

    session: Mapped["CvAnalysisSessionEntity"] = relationship(
        back_populates="skill_gaps"
    ) # type: ignore 
