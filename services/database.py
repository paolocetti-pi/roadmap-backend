from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from typing import Generator
from contextlib import contextmanager
import logging

load_dotenv()

class DatabaseService:
    """Database service class for managing database connections and operations"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            # Use SQLite as default if no DATABASE_URL is provided
            self.database_url = "sqlite:///./star_wars.db"
            logging.warning("DATABASE_URL not set, using default SQLite database")
        
        logging.info(f"Connecting to database: {self.database_url}")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup"""
        logging.debug("Opening new database session")
        db = self.SessionLocal()
        try:
            yield db
        finally:
            logging.debug("Closing database session")
            db.close()
    
    @contextmanager
    def get_db_context(self) -> Session:
        """Get database session as context manager"""
        logging.debug("Opening new database session with context manager")
        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            logging.error(f"Database error occurred: {e}. Rolling back.")
            db.rollback()
            raise
        finally:
            logging.debug("Closing database session from context manager")
            db.close()
    
    def init_db(self):
        """Initialize database tables"""
        from models.base import Base
        logging.info("Initializing database tables")
        try:
            Base.metadata.create_all(bind=self.engine)
            logging.info("Database tables initialized successfully")
        except Exception as e:
            logging.critical(f"Failed to initialize database tables: {e}")
            raise
    
    def drop_db(self):
        """Drop all database tables"""
        from models.base import Base
        logging.warning("Dropping all database tables")
        try:
            Base.metadata.drop_all(bind=self.engine)
            logging.info("Database tables dropped successfully")
        except Exception as e:
            logging.critical(f"Failed to drop database tables: {e}")
            raise

# Global database service instance
database_service = DatabaseService()

# Convenience function for dependency injection
def get_db() -> Generator[Session, None, None]:
    """Dependency injection function for FastAPI"""
    yield from database_service.get_db()

# Convenience function for initialization
def init_db():
    database_service.init_db() 