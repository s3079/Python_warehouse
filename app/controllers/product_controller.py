from app.models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self._model = ProductModel()
    
    def get_all_products(self):
        """Get all products with their category and supplier names"""
        try:
            products = self._model.get_all()
            if not products:
                return []
            
            # Results are already in dictionary format from the model
            formatted_products = []
            for product in products:
                product_dict = {
                    "product_id": product["product_id"],
                    "name": product["name"],
                    "description": product["description"] if product["description"] else "",
                    "unit_price": product["unit_price"],
                    "category_id": product["category_id"],
                    "supplier_id": product["supplier_id"],
                    "created_at": product["created_at"],
                    "updated_at": product["updated_at"],
                    "category_name": product["category_name"] if product["category_name"] else "",
                    "supplier_name": product["supplier_name"] if product["supplier_name"] else ""
                }
                formatted_products.append(product_dict)
            return formatted_products
        except Exception as e:
            self.handle_error(e, "getting all products")
            return []
    
    def add_product(self, data):
        """Add a new product"""
        try:
            if not data.get('name'):
                raise ValueError("Product name is required")
            return self._model.add(**data)
        except Exception as e:
            self.handle_error(e, "adding product")
            raise
    
    def update_product(self, product_id, data):
        """Update an existing product"""
        try:
            if not product_id:
                raise ValueError("Product ID is required")
            if not data.get('name'):
                raise ValueError("Product name is required")
            return self._model.update(product_id=product_id, **data)
        except Exception as e:
            self.handle_error(e, "updating product")
            raise
    
    def delete_product(self, product_id):
        """Delete a product"""
        try:
            if not product_id:
                raise ValueError("Product ID is required")
            return self._model.delete(product_id)
        except Exception as e:
            self.handle_error(e, "deleting product")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Error {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message
    
    def get_products_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated products with optional search"""
        try:
            return self._model.get_products_paginated(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "getting paginated products")
            return [], 0