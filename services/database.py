from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from typing import AsyncGenerator
import logging
from fastapi import Request, FastAPI

load_dotenv()

class DatabaseService:
    """Database service class for managing database connections and operations"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            # Use SQLite as default if no DATABASE_URL is provided
            self.database_url = "sqlite+aiosqlite:///./star_wars.db"
            logging.warning("DATABASE_URL not set, using default SQLite database")
        
        # Add async driver if not present
        if "sqlite" in self.database_url and "sqlite+" not in self.database_url:
            self.database_url = self.database_url.replace("sqlite://", "sqlite+aiosqlite://")
        elif "postgresql" in self.database_url and "postgresql+" not in self.database_url:
            self.database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        elif "mysql" in self.database_url:
            if "mysql+pymysql" in self.database_url:
                self.database_url = self.database_url.replace("mysql+pymysql", "mysql+asyncmy")
            elif "mysql://" in self.database_url:
                self.database_url = self.database_url.replace("mysql://", "mysql+asyncmy://")

        logging.info(f"Connecting to database: {self.database_url}")
        self.engine = create_async_engine(self.database_url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
        )
    
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup"""
        logging.debug("Opening new database session")
        async with self.SessionLocal() as session:
            try:
                yield session
            finally:
                logging.debug("Closing database session")
                await session.close()

    async def init_db(self):
        """Initialize database tables"""
        from models.base import Base
        logging.info("Initializing database tables")
        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.create_all)
                logging.info("Database tables initialized successfully")
            except Exception as e:
                logging.critical(f"Failed to initialize database tables: {e}")
                raise
    
    async def drop_db(self):
        """Drop all database tables"""
        from models.base import Base
        logging.warning("Dropping all database tables")
        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
                logging.info("Database tables dropped successfully")
            except Exception as e:
                logging.critical(f"Failed to drop database tables: {e}")
                raise

# Convenience function for dependency injection
async def get_db(request: "Request") -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection function for FastAPI"""
    database_service: "DatabaseService" = request.app.state.database_service
    async for session in database_service.get_db():
        yield session

# Convenience function for initialization
async def init_db(app: "FastAPI"):
    database_service = DatabaseService()
    await database_service.init_db()
    app.state.database_service = database_service 