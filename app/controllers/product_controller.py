from app.controllers.base_controller import BaseController
from app.models.product_model import ProductModel

class ProductController(BaseController):
    def __init__(self, parent=None):
        super().__init__()
        self._model = ProductModel()
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        """Initialize the controller"""
        pass
    
    def get_all(self):
        """Get all products"""
        try:
            return self._model.get_all()
        except Exception as e:
            self.handle_error(e, "getting products")
            return []
    
    def add_product(self, data):
        """Add a new product"""
        try:
            if not data.get('name'):
                raise ValueError("Product name is required")
            
            self._model.add(**data)
            return True, "Product added successfully"
        except Exception as e:
            self.handle_error(e, "adding product")
            return False, str(e)
    
    def update_product(self, product_id, data):
        """Update an existing product"""
        try:
            if not data.get('name'):
                raise ValueError("Product name is required")
            
            data['product_id'] = product_id
            self._model.update(**data)
            return True, "Product updated successfully"
        except Exception as e:
            self.handle_error(e, "updating product")
            return False, str(e)
    
    def delete_product(self, product_id):
        """Delete a product"""
        try:
            self._model.delete(product_id)
            return True, "Product deleted successfully"
        except Exception as e:
            self.handle_error(e, "deleting product")
            return False, str(e)
    
    def get_product(self, product_id):
        """Get a product by ID"""
        try:
            return self._model.get_by_id(product_id)
        except Exception as e:
            self.handle_error(e, "getting product")
            return None
    
    def search_products(self, query):
        """Search products by name or model"""
        try:
            return self._model.search(query)
        except Exception as e:
            self.handle_error(e, "searching products")
            return []
    
    def filter_products(self, filters):
        """Filter products by various criteria"""
        try:
            return self._model.filter(**filters)
        except Exception as e:
            self.handle_error(e, "filtering products")
            return []
    
    def get_all_products(self):
        """Get all products with their category and supplier names"""
        products = self._model.get_all()
        # Convert tuple results to dictionaries for easier access
        formatted_products = []
        for product in products:
            formatted_products.append({
                "product_id": product[0],
                "name": product[1],
                "description": product[2],
                "unit_price": product[3],
                "category_id": product[4],
                "supplier_id": product[5],
                "created_at": product[6],
                "updated_at": product[7],
                "category_name": product[8],
                "supplier_name": product[9]
            })
        return formatted_products
