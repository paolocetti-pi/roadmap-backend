from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services.database import get_db


class BaseRouter:
    """Base router class with common functionality for all routers"""
    
    def __init__(self, prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup all routes for this router - to be overridden by subclasses"""
        pass
    
    def get_db_session(self) -> Session:
        """Get database session for dependency injection"""
        return Depends(get_db)
    
    def handle_exception(self, e: Exception) -> HTTPException:
        """Handle exceptions and return appropriate HTTP responses"""
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router instance"""
        return self.router 