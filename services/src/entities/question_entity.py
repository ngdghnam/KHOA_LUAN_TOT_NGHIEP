import uuid
from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.base_entity import BaseEntity

class QuestionEntity(BaseEntity):
    __tablename__ = "questions"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cv_analysis_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Optional: để giữ thứ tự câu hỏi
    order_index: Mapped[int] = mapped_column(Integer, nullable=True)

    session: Mapped["CvAnalysisSessionEntity"] = relationship(
        back_populates="questions"
    )
