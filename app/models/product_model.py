from app.models.base_model import BaseModel

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "products"
    
    def get_all(self):
        """Get all products with category and supplier names"""
        query = f"""
            SELECT 
                p.product_id, 
                p.name, 
                p.description, 
                p.unit_price,
                p.category_id, 
                p.supplier_id, 
                p.created_at, 
                p.updated_at,
                c.name as category_name, 
                s.name as supplier_name
            FROM {self._table_name} p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.name
        """
        try:
            return self._execute_query(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def add(self, **data):
        """Add a new product"""
        query = f"""
            INSERT INTO {self._table_name} 
            (name, description, unit_price, category_id, supplier_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('name'),
            data.get('description'),
            data.get('unit_price'),
            data.get('category_id'),
            data.get('supplier_id')
        )
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True, "Product added successfully"
        return False, "Failed to add product"
    
    def get_all_with_names(self):
        """Get all products with category and supplier names"""
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.unit_price,
                p.category_id,
                p.supplier_id,
                c.name as category_name,
                s.name as supplier_name
            FROM {self._table_name} p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.name
        """
        cursor = self._execute_query(query)
        return cursor.fetchall() if cursor else []
    
    def update(self, product_id: int, name: str, description: str, 
               unit_price: float, category_id: int = None, supplier_id: int = None):
        """Update an existing product"""
        query = f"""
            UPDATE {self._table_name}
            SET name = %s, description = %s, unit_price = %s, 
                category_id = %s, supplier_id = %s
            WHERE product_id = %s
        """
        cursor = self._execute_query(query, (name, description, unit_price, 
                                         category_id, supplier_id, product_id))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def delete(self, product_id: int):
        """Delete a product"""
        query = f"DELETE FROM {self._table_name} WHERE product_id = %s"
        cursor = self._execute_query(query, (product_id,))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def get_by_id(self, product_id: int):
        """Get a product by ID with category and supplier names"""
        query = f"""
            SELECT 
                p.product_id, p.name, p.description, p.unit_price,
                p.category_id, p.supplier_id, p.created_at, p.updated_at,
                c.name as category_name, s.name as supplier_name
            FROM {self._table_name} p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_id = %s
        """
        cursor = self._execute_query(query, (product_id,))
        return cursor.fetchone() if cursor else None
    
    def get_products_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated products with optional search"""
        try:
            # Base query
            query = """
                SELECT p.*, c.name as category_name, s.name as supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            """
            count_query = "SELECT COUNT(*) FROM products p"
            
            params = []
            
            # Add search condition if search_query is provided
            if search_query:
                query += " WHERE p.name LIKE %s OR p.description LIKE %s"
                count_query += " WHERE p.name LIKE %s OR p.description LIKE %s"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Get total count
            cursor = self.conn.cursor()
            if search_query:
                cursor.execute(count_query, [f"%{search_query}%", f"%{search_query}%"])
            else:
                cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            # Get paginated results
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            products = [dict(zip(columns, product)) for product in products]
            
            return products, total_count
            
        except Exception as e:
            print(f"Error getting paginated products: {e}")
            return [], 0