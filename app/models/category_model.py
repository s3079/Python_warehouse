from app.utils.database import Database
from app.models.base_model import BaseModel

class CategoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "categories"
        self._db = Database()
        self._db.connect()  # Ensure connection is established
    
    def _execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if not self._db._connection or not self._db._connection.is_connected():
                self._db.connect()
            return self._db.execute_query(query, params)
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def get_all(self):
        """Get all categories"""
        query = f"""
            SELECT 
                category_id, name, description, created_at, updated_at
            FROM {self._table_name}
            ORDER BY name
        """
        return self._execute_query(query) or []
        
    def count_products(self, category_id):
        """Count number of products in a category"""
        query = """
            SELECT COUNT(*) as count
            FROM products 
            WHERE category_id = %s
        """
        result = self._execute_query(query, (category_id,))
        return result[0]['count'] if result else 0
        
    def add(self, name: str, description: str):
        """Add a new category"""
        query = f"INSERT INTO {self._table_name} (name, description) VALUES (%s, %s)"
        return self._execute_query(query, (name, description))
    
    def update(self, category_id: int, name: str, description: str):
        """Update a category"""
        query = f"UPDATE {self._table_name} SET name = %s, description = %s WHERE category_id = %s"
        return self._execute_query(query, (name, description, category_id))
    
    def delete(self, category_id: int):
        """Delete a category"""
        query = f"DELETE FROM {self._table_name} WHERE category_id = %s"
        return self._execute_query(query, (category_id,))
    
    def get_by_id(self, category_id: int):
        """Get a category by id"""
        query = f"SELECT * FROM {self._table_name} WHERE category_id = %s"
        result = self._execute_query(query, (category_id,))
        return result[0] if result else None
    
    def get_all_categories(self):
        """Get all categories"""
        query = f"SELECT category_id, name FROM {self._table_name} ORDER BY name"
        try:
            return self._execute_query(query) or []
        except Exception as e:
            print(f"Error in get_all_categories: {str(e)}")
            return []
