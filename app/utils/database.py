import mysql.connector
from mysql.connector import Error
from app.config.config import Config

class Database:
    """Database connection handler with connection pooling"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def connect(self):
        """Establish database connection"""
        if not self._connection or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    **Config.get_db_config(),
                    autocommit=False
                )
            except Error as e:
                raise Exception(f"Database connection error: {str(e)}")
    
    def disconnect(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self._connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                result = cursor.fetchall()
            else:
                self._connection.commit()
                result = cursor.rowcount
                
            cursor.close()
            return result
            
        except Error as e:
            self._connection.rollback()
            raise Exception(f"Query execution error: {str(e)}")
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed"""
        self.disconnect()
