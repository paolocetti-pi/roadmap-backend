from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from fastapi import HTTPException


class BaseService:
    """Base service class with common CRUD operations"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self, db: Session) -> List[Dict[str, Any]]:
        """Get all records from the database"""
        try:
            records = db.query(self.model_class).all()
            return [record.to_dict() for record in records]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving records: {str(e)}")
    
    def get_by_id(self, db: Session, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a record by its ID"""
        try:
            record = db.query(self.model_class).filter(self.model_class.id == record_id).first()
            if not record:
                raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
            return record.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving record: {str(e)}")
    
    def create(self, db: Session, data: dict) -> Dict[str, Any]:
        """Create a new record"""
        try:
            record = self.model_class.from_dict(data)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record.to_dict()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating record: {str(e)}")
    
    def update(self, db: Session, record_id: int, data: dict) -> Dict[str, Any]:
        """Update an existing record"""
        try:
            record = db.query(self.model_class).filter(self.model_class.id == record_id).first()
            if not record:
                raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
            
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            
            db.commit()
            db.refresh(record)
            return record.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating record: {str(e)}")
    
    def delete(self, db: Session, record_id: int) -> bool:
        """Delete a record by its ID"""
        try:
            record = db.query(self.model_class).filter(self.model_class.id == record_id).first()
            if not record:
                raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
            
            db.delete(record)
            db.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting record: {str(e)}")
    
    def validate_data(self, data: dict) -> bool:
        """Validate data before creating or updating records - to be overridden by subclasses"""
        return True 