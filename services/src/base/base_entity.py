from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()

class BaseEntity(Base):
    __abstract__ = True 
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
