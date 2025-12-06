from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from contextlib import asynccontextmanager
from src.config.environments import settings

Base = declarative_base()

class Database:
    def __init__(self):
        # Change to async driver: mysql+aiomysql or mysql+asyncmy
        self.DATABASE_URL = (
            f"mysql+aiomysql://"
            f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/"
            f"{settings.DB_NAME}"
        )
        
        self.engine = create_async_engine(
            self.DATABASE_URL,
            echo=False,
            # pool_pre_ping=True,
            # pool_recycle=3600,
        )
        
        self.AsyncSessionLocal = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    # For FastAPI dependency injection
    async def get_db(self):
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
                
    async def check_connection(self):
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("Database connected successfully!")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

# Global instance
database = Database()