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
        """Delete an order and its details"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # First delete from order_details (child table)
            details_query = "DELETE FROM order_details WHERE order_id = %s"
            cursor.execute(details_query, (order_id,))
            
            # Then delete from orders (parent table)
            order_query = f"DELETE FROM {self._table_name} WHERE order_id = %s"
            cursor.execute(order_query, (order_id,))
            
            # Commit the transaction
            self.conn.commit()
            return True
            
        except Exception as e:
            # Rollback in case of error
            self.conn.rollback()
            print(f"Error deleting order: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def add(self, order_date, total_amount, user_id):
        """Add a new order"""
        query = f"""
            INSERT INTO {self._table_name} 
            (order_date, total_amount, user_id)
            VALUES (%s, %s, %s)
        """
        params = (order_date, total_amount, user_id)
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
                od.quantity,
                od.unit_price,
                u.username as buyer_name,
                p.name as product_name,
                p.product_id
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
    
    def add_order_detail(self, order_id, product_id, quantity, unit_price):
        """Add a new order detail"""
        query = f"""
            INSERT INTO order_details 
            (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
        """
        params = (order_id, product_id, quantity, unit_price)
        cursor = self._execute_query(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False 
    
    def get_order_detail(self, order_id):
        """Get detailed order information including product details"""
        query = """
            SELECT 
                o.id,
                o.order_date,
                o.total_amount,
                o.quantity,
                o.unit_price,
                o.product_id,
                p.product_name,
                u.username as user_name
            FROM orders o
            JOIN products p ON o.product_id = p.id
            JOIN users u ON o.user_id = u.id
            WHERE o.id = %s
        """
        cursor = self._execute_query(query, (order_id,))
        if cursor:
            return cursor.fetchone()
        return None 
    
    def update_order(self, order_id, order_date, quantity, total_amount, product_id, user_id, unit_price):
        """Update an existing order and its details"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # Update main order
            order_query = f"""
                UPDATE {self._table_name}
                SET order_date = %s,
                    total_amount = %s,
                    user_id = %s
                WHERE order_id = %s
            """
            cursor.execute(order_query, (order_date, total_amount, user_id, order_id))
            
            # Update order details
            details_query = """
                UPDATE order_details
                SET quantity = %s,
                    product_id = %s,
                    unit_price = %s
                WHERE order_id = %s
            """
            cursor.execute(details_query, (quantity, product_id, unit_price, order_id))
            
            # Commit changes
            self.conn.commit()
            return True
            
        except Exception as e:
            # Rollback in case of error
            self.conn.rollback()
            print(f"Error updating order: {e}")
            return False
        finally:
            if cursor:
                cursor.close() 