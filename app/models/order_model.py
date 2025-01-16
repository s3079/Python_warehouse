from app.models.base_model import BaseModel

class OrderModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "orders"
    
    def get_all(self):
        """Get all orders with customer and status details"""
        query = f"""
            SELECT 
                o.order_id, 
                o.customer_name, 
                o.order_date, 
                o.total_amount,
                o.status,
                o.created_at, 
                o.updated_at
            FROM {self._table_name} o
            ORDER BY o.order_date DESC
        """
        try:
            return self._execute_query(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def get_orders_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated orders with optional search"""
        try:
            # Base query
            query = f"""
                SELECT o.*
                FROM {self._table_name} o
            """
            count_query = f"SELECT COUNT(*) FROM {self._table_name} o"
            
            params = []
            
            # Add search condition if search_query is provided
            if search_query:
                query += " WHERE o.customer_name LIKE %s OR o.status LIKE %s"
                count_query += " WHERE o.customer_name LIKE %s OR o.status LIKE %s"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            
            # Add pagination
            query += " ORDER BY o.order_date DESC LIMIT %s OFFSET %s"
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
            orders = cursor.fetchall()
            
            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            orders = [dict(zip(columns, order)) for order in orders]
            
            return orders, total_count
            
        except Exception as e:
            print(f"Error getting paginated orders: {e}")
            return [], 0
    
    def update(self, order_id: int, data: dict):
        """Update an existing order"""
        query = f"""
            UPDATE {self._table_name}
            SET customer_name = %s, order_date = %s, total_amount = %s, status = %s
            WHERE order_id = %s
        """
        params = (
            data.get('customer_name'),
            data.get('order_date'),
            data.get('total_amount'),
            data.get('status'),
            order_id
        )
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def delete(self, order_id: int):
        """Delete an order"""
        query = f"DELETE FROM {self._table_name} WHERE order_id = %s"
        cursor = self._execute_query(query, (order_id,))
        if cursor:
            self.conn.commit()
            return True
        return False 