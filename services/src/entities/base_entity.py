from sqlalchemy import Column, String, DateTime, Boolean, TypeDecorator
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.dialects.mysql import CHAR
import uuid
from datetime import datetime

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses CHAR(36) for MySQL.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

class Base(DeclarativeBase):
    pass

class BaseEntity(Base):
    __abstract__ = True 
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=True)
