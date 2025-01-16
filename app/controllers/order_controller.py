from app.models.order_model import OrderModel

class OrderController:
    def __init__(self):
        self._model = OrderModel()
    
    def get_orders_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated orders with optional search"""
        try:
            return self._model.get_orders_paginated(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "getting paginated orders")
            return [], 0
    
    def update_order(self, order_id, data):
        """Update an existing order"""
        try:
            if not order_id:
                raise ValueError("Order ID is required")
            return self._model.update(order_id, data)
        except Exception as e:
            self.handle_error(e, "updating order")
            raise
    
    def delete_order(self, order_id):
        """Delete an order"""
        try:
            if not order_id:
                raise ValueError("Order ID is required")
            return self._model.delete(order_id)
        except Exception as e:
            self.handle_error(e, "deleting order")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Error {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message 
    
    def get_order_details(self, order_id):
        """Get detailed information for a specific order"""
        try:
            return self._model.get_order_details(order_id)
        except Exception as e:
            self.handle_error(e, "getting order details")
            return None 