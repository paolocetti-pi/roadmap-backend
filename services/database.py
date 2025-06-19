from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from typing import Generator
from contextlib import contextmanager

load_dotenv()

class DatabaseService:
    """Database service class for managing database connections and operations"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            # Use SQLite as default if no DATABASE_URL is provided
            self.database_url = "sqlite:///./star_wars.db"
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    @contextmanager
    def get_db_context(self) -> Session:
        """Get database session as context manager"""
        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    
    def init_db(self):
        """Initialize database tables"""
        from models.base import Base
        Base.metadata.create_all(bind=self.engine)
    
    def drop_db(self):
        """Drop all database tables"""
        from models.base import Base
        Base.metadata.drop_all(bind=self.engine)

# Global database service instance
database_service = DatabaseService()

# Convenience function for dependency injection
def get_db() -> Generator[Session, None, None]:
    """Dependency injection function for FastAPI"""
    yield from database_service.get_db()

# Convenience function for initialization
def init_db():
    database_service.init_db() 