from app.models.inventory_model import InventoryModel

class InventoryController:
    def __init__(self):
        self._model = InventoryModel()
    
    def get_all_inventory(self):
        """Get all inventory items with product details"""
        try:
            inventory_items = self._model.get_all()
            if not inventory_items:
                return []
                
            # Format inventory items
            formatted_inventory = []
            for item in inventory_items:
                item_dict = {
                    "inventory_id": item["inventory_id"],
                    "product_name": item["product_name"],
                    "quantity": item["quantity"],
                    "category_name": item["category_name"] if item["category_name"] else "",
                    "supplier_name": item["supplier_name"] if item["supplier_name"] else "",
                    "unit_price": item["unit_price"],
                }
                formatted_inventory.append(item_dict)
            return formatted_inventory
        except Exception as e:
            print(f"Error getting inventory: {e}")
            self.handle_error(e, "getting inventory")
            return []
    
    def add_inventory(self, product_id, quantity=0):
        """Add a new inventory item"""
        try:
            if not product_id:
                raise ValueError("Product ID is required")
            return self._model.add(product_id, quantity)
        except Exception as e:
            self.handle_error(e, "adding inventory item")
            raise
    
    def update_inventory(self, inventory_id, quantity):
        """Update an existing inventory item"""
        try:
            if not inventory_id:
                raise ValueError("Inventory ID is required")
            return self._model.update(inventory_id, quantity)
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
    
    def get_product_names(self):
        """Retrieve a list of all product names"""
        try:
            # Assuming you have a method in your model to get all products
            products = self._model.get_all_products()
            return [product["name"] for product in products]
        except Exception as e:
            print(f"Error getting product names: {e}")
            self.handle_error(e, "getting product names")
            return []