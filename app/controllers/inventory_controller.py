from app.models.inventory_model import InventoryModel
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel

class InventoryController:
    def __init__(self):
        self._model = InventoryModel()
        self._category_model = CategoryModel()
        self._product_model = ProductModel()
    
    def get_all_inventory(self):
        """Get all inventory items with their product names"""
        try:
            inventory = self._model.get_all()
            if not inventory:
                return []
            
            formatted_inventory = []
            for item in inventory:
                item_dict = {
                    "inventory_id": item["inventory_id"],
                    "product_name": item["product_name"],
                    "quantity": item["quantity"]
                }
                formatted_inventory.append(item_dict)
            return formatted_inventory
        except Exception as e:
            self.handle_error(e, "getting all inventory items")
            return []
    
    def add_inventory(self, data):
        """Add a new inventory item"""
        try:
            if 'product_id' not in data:
                raise ValueError("Product ID is required")
            return self._model.add(**data)
        except Exception as e:
            self.handle_error(e, "adding inventory item")
            raise
    
    def update_inventory(self, inventory_id, data):
        """Update an existing inventory item"""
        try:
            if not inventory_id:
                raise ValueError("Inventory ID is required")
            if not data.get('product_id'):
                raise ValueError("Product ID is required")
            return self._model.update(inventory_id=inventory_id, **data)
        except Exception as e:
            self.handle_error(e, "updating inventory item")
            raise
    
    def delete_inventory(self, inventory_id):
        """Delete an inventory item"""
        try:
            if not inventory_id:
                raise ValueError("Inventory ID is required")
            return self._model.delete(inventory_id)
        except Exception as e:
            self.handle_error(e, "deleting inventory item")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Error {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message
    
    def get_inventory_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated inventory items with optional search"""
        try:
            return self._model.get_inventory_paginated(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "getting paginated inventory items")
            return [], 0
    
    def get_category_names(self):
        """Get all category names"""
        try:
            categories = self._category_model.get_all_categories()
            return [category['name'] for category in categories]
        except Exception as e:
            self.handle_error(e, "getting category names")
            return []
    
    def get_product_names(self):
        """Get all product names"""
        try:
            products = self._product_model.get_all_products()
            return [product['name'] for product in products]
        except Exception as e:
            self.handle_error(e, "getting product names")
            return []
    
    def get_product_id_by_name(self, product_name):
        """Get product ID by product name"""
        try:
            product = self._product_model.get_by_name(product_name)
            return product['product_id'] if product else None
        except Exception as e:
            self.handle_error(e, "getting product ID by name")
            return None