from app.models.base_model import BaseModel

class SupplierModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "suppliers"
    
    def get_all(self):
        """Get all suppliers"""
        query = f"SELECT * FROM {self._table_name} ORDER BY name"
        return self._execute_query(query)
    
    def add(self, name: str, contact_name: str = None, address: str = None, 
            phone: str = None, email: str = None):
        """Add a new supplier"""
        query = f"""
            INSERT INTO {self._table_name} 
            (name, contact_name, address, phone, email) 
            VALUES (%s, %s, %s, %s, %s)
        """
        return self._execute_query(query, (name, contact_name, address, phone, email))
    
    def update(self, supplier_id: int, name: str, contact_name: str = None, 
              address: str = None, phone: str = None, email: str = None):
        """Update an existing supplier"""
        query = f"""
            UPDATE {self._table_name} 
            SET name = %s, contact_name = %s, address = %s, phone = %s, email = %s 
            WHERE supplier_id = %s
        """
        return self._execute_query(query, (name, contact_name, address, phone, email, supplier_id))
    
    def delete(self, supplier_id: int):
        """Delete a supplier"""
        query = f"DELETE FROM {self._table_name} WHERE supplier_id = %s"
        return self._execute_query(query, (supplier_id,))
    
    def get_by_id(self, supplier_id: int):
        """Get a supplier by ID"""
        query = f"SELECT * FROM {self._table_name} WHERE supplier_id = %s"
        result = self._execute_query(query, (supplier_id,))
        return result[0] if result else None
