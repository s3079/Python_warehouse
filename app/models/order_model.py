from app.models.base_model import BaseModel

class OrderModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "orders"
    
    def get_all(self):
        """Get all orders"""
        query = f"""
            SELECT 
                o.order_id, 
                o.order_date, 
                o.total_amount,
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
            
            # Add pagination
            query += " ORDER BY o.order_date DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Get total count
            cursor = self.conn.cursor()
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
            SET order_date = %s, total_amount = %s
            WHERE order_id = %s
        """
        params = (
            data.get('order_date'),
            data.get('total_amount'),
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
    
    def add(self, order_date, total_amount):
        """Add a new order"""
        query = f"""
            INSERT INTO {self._table_name} 
            (order_date, total_amount)
            VALUES (%s, %s)
        """
        params = (order_date, total_amount)
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False 
    
    def get_order_details(self, order_id):
        """Get detailed information for a specific order"""
        query = f"""
            SELECT 
                o.order_id, 
                o.order_date, 
                o.total_amount,
                u.username as buyer_name,
                p.name as product_name
            FROM {self._table_name} o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_details od ON o.order_id = od.order_id
            JOIN products p ON od.product_id = p.product_id
            WHERE o.order_id = %s
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            if result:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, result))
            return None
        except Exception as e:
            print(f"Error getting order details: {e}")
            return None 