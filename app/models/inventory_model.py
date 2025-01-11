from app.models.base_model import BaseModel

class InventoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "inventory"
    
    def get_all(self):
        """Get all inventory items with product details"""
        query = f"""
            SELECT i.*, p.name as product_name, p.unit_price,
                   c.name as category_name, s.name as supplier_name
            FROM {self._table_name} i
            JOIN products p ON i.product_id = p.product_id
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.name
        """
        return self._execute_query(query)
    
    def add(self, product_id: int, quantity: int = 0):
        """Add a new inventory item"""
        query = f"""
            INSERT INTO {self._table_name} (product_id, quantity)
            VALUES (%s, %s)
        """
        return self._execute_query(query, (product_id, quantity))
    
    def update(self, inventory_id: int, quantity: int):
        """Update an inventory item"""
        query = f"""
            UPDATE {self._table_name}
            SET quantity = %s
            WHERE inventory_id = %s
        """
        return self._execute_query(query, (quantity, inventory_id))
    
    def delete(self, inventory_id: int):
        """Delete an inventory item"""
        query = f"DELETE FROM {self._table_name} WHERE inventory_id = %s"
        return self._execute_query(query, (inventory_id,))
    
    def update_quantity(self, product_id: int, quantity: int):
        """Update product quantity"""
        # First check if inventory record exists
        check_query = f"SELECT inventory_id FROM {self._table_name} WHERE product_id = %s"
        result = self._execute_query(check_query, (product_id,))
        
        if result:
            # Update existing record
            query = f"""
                UPDATE {self._table_name}
                SET quantity = %s
                WHERE product_id = %s
            """
            return self._execute_query(query, (quantity, product_id))
        else:
            # Insert new record
            return self.add(product_id, quantity)
    
    def get_by_product_id(self, product_id: int):
        """Get inventory item by product ID"""
        query = f"""
            SELECT i.*, p.name as product_name, p.unit_price,
                   c.name as category_name, s.name as supplier_name
            FROM {self._table_name} i
            JOIN products p ON i.product_id = p.product_id
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE i.product_id = %s
        """
        result = self._execute_query(query, (product_id,))
        return result[0] if result else None
    
    def get_low_stock_items(self, threshold: int = 10):
        """Get items with quantity below threshold"""
        query = f"""
            SELECT i.*, p.name as product_name, p.unit_price,
                   c.name as category_name, s.name as supplier_name
            FROM {self._table_name} i
            JOIN products p ON i.product_id = p.product_id
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE i.quantity <= %s
            ORDER BY i.quantity ASC
        """
        return self._execute_query(query, (threshold,))
    
    def get_all_products(self):
        """Get all products"""
        query = "SELECT product_id, name FROM products ORDER BY name"
        return self._execute_query(query)