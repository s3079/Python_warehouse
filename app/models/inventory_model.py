from app.models.base_model import BaseModel

class InventoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "inventory"
    
    def get_all(self):
        """Get all inventory items with category and supplier names"""
        query = f"""
            SELECT 
                i.inventory_id, 
                i.product_name, 
                i.quantity, 
                i.category_id, 
                c.name as category_name
            FROM {self._table_name} i
            LEFT JOIN categories c ON i.category_id = c.category_id
            ORDER BY i.product_name
        """
        try:
            return self._execute_query(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def add(self, **data):
        """Add a new inventory item"""
        query = f"""
            INSERT INTO {self._table_name} 
            (product_name, quantity, category_id, supplier_id)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data.get('product_name'),
            data.get('quantity'),
            data.get('category_id'),
            data.get('supplier_id')
        )
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True, "Inventory item added successfully"
        return False, "Failed to add inventory item"
    
    def update(self, inventory_id: int, product_name: str, quantity: int, 
               category_id: int = None, supplier_id: int = None):
        """Update an existing inventory item"""
        query = f"""
            UPDATE {self._table_name}
            SET product_name = %s, quantity = %s, 
                category_id = %s, supplier_id = %s
            WHERE inventory_id = %s
        """
        cursor = self._execute_query(query, (product_name, quantity, 
                                             category_id, supplier_id, inventory_id))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def delete(self, inventory_id: int):
        """Delete an inventory item"""
        query = f"DELETE FROM {self._table_name} WHERE inventory_id = %s"
        cursor = self._execute_query(query, (inventory_id,))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def get_by_id(self, inventory_id: int):
        """Get an inventory item by ID with category name"""
        query = f"""
            SELECT 
                i.inventory_id, i.product_name, i.quantity,
                i.category_id,
                c.name as category_name
            FROM {self._table_name} i
            LEFT JOIN categories c ON i.category_id = c.category_id
            WHERE i.inventory_id = %s
        """
        cursor = self._execute_query(query, (inventory_id,))
        return cursor.fetchone() if cursor else None
    
    def get_inventory_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated inventory items with optional search"""
        try:
            query = """
                SELECT i.*, c.name as category_name
                FROM inventory i
                LEFT JOIN categories c ON i.category_id = c.category_id
            """
            count_query = "SELECT COUNT(*) FROM inventory i"
            
            params = []
            
            if search_query:
                query += " WHERE i.product_name LIKE %s"
                count_query += " WHERE i.product_name LIKE %s"
                params.append(f"%{search_query}%")
            
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor = self.conn.cursor()
            if search_query:
                cursor.execute(count_query, [f"%{search_query}%"])
            else:
                cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            cursor.execute(query, params)
            inventory = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            inventory = [dict(zip(columns, item)) for item in inventory]
            
            return inventory, total_count
            
        except Exception as e:
            print(f"Error getting paginated inventory: {e}")
            return [], 0