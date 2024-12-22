from app.models.base_model import BaseModel

class CategoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "categories"
    
    def get_all(self):
        """Get all categories"""
        query = f"SELECT * FROM {self._table_name} ORDER BY name"
        return self._execute_query(query)
    
    def add(self, name: str, description: str):
        """Add a new category"""
        query = f"INSERT INTO {self._table_name} (name, description) VALUES (%s, %s)"
        return self._execute_query(query, (name, description))
    
    def update(self, category_id: int, name: str, description: str):
        """Update an existing category"""
        query = f"UPDATE {self._table_name} SET name = %s, description = %s WHERE category_id = %s"
        return self._execute_query(query, (name, description, category_id))
    
    def delete(self, category_id: int):
        """Delete a category"""
        query = f"DELETE FROM {self._table_name} WHERE category_id = %s"
        return self._execute_query(query, (category_id,))
    
    def get_by_id(self, category_id: int):
        """Get a category by ID"""
        query = f"SELECT * FROM {self._table_name} WHERE category_id = %s"
        result = self._execute_query(query, (category_id,))
        return result[0] if result else None
