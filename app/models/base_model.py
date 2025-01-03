from abc import ABC, abstractmethod
import mysql.connector
from app.config.config import Config

class BaseModel(ABC):
    """Abstract base class for all models"""
    
    def __init__(self):
        """Initialize database connection"""
        self.config = Config.get_db_config()
        self._connect()

    def _connect(self):
        """Create database connection"""
        try:
            self.conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            # Use dictionary cursor by default
            self.conn.cursor_class = mysql.connector.cursor.MySQLCursorDict
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            self.conn = None
    
    def __del__(self):
        """Close database connection"""
        try:
            if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
                self.conn.close()
        except:
            pass  # Ignore errors during cleanup
    
    def _execute_query(self, query, params=None):
        """Protected method to execute database queries"""
        cursor = None
        try:
            if not self.conn or not self.conn.is_connected():
                self._connect()
            
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            # For SELECT queries, return the results
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            
            # For other queries (INSERT, UPDATE, DELETE), commit and return cursor
            self.conn.commit()
            return cursor
            
        except mysql.connector.Error as e:
            print(f"Database error: {str(e)}")
            raise
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    @abstractmethod
    def get_all(self):
        """Get all records"""
        pass
    
    @abstractmethod
    def add(self, data):
        """Add a new record"""
        pass
    
    @abstractmethod
    def update(self, id, data):
        """Update a record"""
        pass
    
    @abstractmethod
    def delete(self, id):
        """Delete a record"""
        pass
