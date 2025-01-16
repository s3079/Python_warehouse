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
    
    def update_order(self, data):
        """Update an existing order"""
        try:
            # Validate data
            if not all(key in data for key in ['order_id', 'order_date', 'quantity', 'total_amount', 'product_id']):
                raise ValueError("Missing required fields")

            return self._model.update_order(
                order_id=data['order_id'],
                order_date=data['order_date'],
                quantity=data['quantity'],
                total_amount=data['total_amount'],
                product_id=data['product_id'],
                user_id=data['user_id'],
                unit_price=data['unit_price']
            )
        except Exception as e:
            print(f"Error in update_order controller: {e}")
            return False
    
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
    
    def add_order(self, data):
        print("Data:", data)
        """Add a new order and its details"""
        try:
            order_date = data.get("order_date")
            total_amount = data.get("total_amount")
            product_id = data.get("product_id")
            quantity = data.get("quantity")
            unit_price = data.get("unit_price")
            user_id = data.get("user_id")
            
            # Add order and get order_id
            order_id = self._model.add(order_date, total_amount, user_id)
            
            if order_id:
                    self._model.add_order_detail(order_id, product_id, quantity, unit_price)
            else:
                raise ValueError("Failed to add order")
            
            return order_id is not None
        except Exception as e:
            self.handle_error(e, "adding order")
            raise

    def get_product_id_by_name(self, product_name):
        """Get product ID by product name"""
        # Implement logic to retrieve product ID from the database
        pass 