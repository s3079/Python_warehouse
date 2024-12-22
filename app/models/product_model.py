from app.models.base_model import BaseModel

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "products"
    
    def get_all(self):
        """Get all products with category and supplier names"""
        query = f"""
            SELECT p.*, c.name as category_name, s.name as supplier_name
            FROM {self._table_name} p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.name
        """
        return self._execute_query(query)
    
    def add(self, name: str, description: str, price: float, 
            category_id: int = None, supplier_id: int = None):
        """Add a new product"""
        query = f"""
            INSERT INTO {self._table_name} 
            (name, description, price, category_id, supplier_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self._execute_query(query, (name, description, price, category_id, supplier_id))
    
    def update(self, product_id: int, name: str, description: str, 
               price: float, category_id: int = None, supplier_id: int = None):
        """Update an existing product"""
        query = f"""
            UPDATE {self._table_name}
            SET name = %s, description = %s, price = %s, 
                category_id = %s, supplier_id = %s
            WHERE product_id = %s
        """
        return self._execute_query(query, (name, description, price, 
                                         category_id, supplier_id, product_id))
    
    def delete(self, product_id: int):
        """Delete a product"""
        query = f"DELETE FROM {self._table_name} WHERE product_id = %s"
        return self._execute_query(query, (product_id,))
    
    def get_by_id(self, product_id: int):
        """Get a product by ID with category and supplier names"""
        query = f"""
            SELECT p.*, c.name as category_name, s.name as supplier_name
            FROM {self._table_name} p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_id = %s
        """
        result = self._execute_query(query, (product_id,))
        return result[0] if result else None
