import uuid
from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.base_entity import BaseEntity


class AnswerEntity(BaseEntity):
    __tablename__ = "answers"

    # 🔥 FK unique để đảm bảo 1-1
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    answer: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationship back
    question: Mapped["QuestionEntity"] = relationship( #type: ignore 
        back_populates="answer"
    )