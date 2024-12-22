from abc import ABC, abstractmethod
from app.utils.database import Database

class BaseModel(ABC):
    """Abstract base class for all models"""
    def __init__(self):
        self._db = Database()
    
    def _execute_query(self, query, params=None):
        """Protected method to execute database queries"""
        try:
            self._db.connect()
            result = self._db.execute_query(query, params)
            return result
        finally:
            self._db.disconnect()
    
    @abstractmethod
    def get_all(self):
        """Abstract method to get all records"""
        pass
    
    @abstractmethod
    def add(self, *args, **kwargs):
        """Abstract method to add a record"""
        pass
    
    @abstractmethod
    def update(self, *args, **kwargs):
        """Abstract method to update a record"""
        pass
    
    @abstractmethod
    def delete(self, id):
        """Abstract method to delete a record"""
        pass
