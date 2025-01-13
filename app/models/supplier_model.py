from app.models.base_model import BaseModel

class SupplierModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "suppliers"
    
    def get_all(self):
        """Get all suppliers"""
        query = f"SELECT * FROM {self._table_name} ORDER BY name"
        try:
            return self._execute_query(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def add(self, **data):
        """Add a new supplier"""
        query = f"""
            INSERT INTO {self._table_name} 
            (name, address, phone, email) 
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data.get('name'),
            data.get('address'),
            data.get('phone'),
            data.get('email')
        )
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True, "Supplier added successfully"
        return False, "Failed to add supplier"
    
    def update(self, supplier_id: int, **data):
        """Update an existing supplier"""
        query = f"""
            UPDATE {self._table_name}
            SET name = %s, address = %s, phone = %s, email = %s
            WHERE supplier_id = %s
        """
        params = (
            data.get('name'),
            data.get('address'),
            data.get('phone'),
            data.get('email'),
            supplier_id
        )
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def delete(self, supplier_id: int):
        """Delete a supplier"""
        query = f"DELETE FROM {self._table_name} WHERE supplier_id = %s"
        cursor = self._execute_query(query, (supplier_id,))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def get_by_id(self, supplier_id: int):
        """Get a supplier by ID"""
        query = f"SELECT * FROM {self._table_name} WHERE supplier_id = %s"
        cursor = self._execute_query(query, (supplier_id,))
        return cursor.fetchone() if cursor else None
    
    def get_suppliers_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated suppliers with optional search"""
        try:
            query = f"SELECT * FROM {self._table_name}"
            count_query = f"SELECT COUNT(*) FROM {self._table_name}"
            
            params = []
            
            if search_query:
                query += " WHERE name LIKE %s OR email LIKE %s"
                count_query += " WHERE name LIKE %s OR email LIKE %s"
                params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
            
            query += " ORDER BY name LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor = self.conn.cursor()
            if search_query:
                cursor.execute(count_query, params[:3])
            else:
                cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            cursor.execute(query, params)
            suppliers = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            suppliers = [dict(zip(columns, supplier)) for supplier in suppliers]
            
            return suppliers, total_count
            
        except Exception as e:
            print(f"Error getting paginated suppliers: {e}")
            return [], 0
