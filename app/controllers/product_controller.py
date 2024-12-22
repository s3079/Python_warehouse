from app.controllers.base_controller import BaseController
from app.models.product_model import ProductModel
from app.models.category_model import CategoryModel
from app.models.supplier_model import SupplierModel
from app.views.product_view import ProductView

class ProductController(BaseController):
    def __init__(self, parent):
        super().__init__()
        self._model = ProductModel()
        self._category_model = CategoryModel()
        self._supplier_model = SupplierModel()
        self._view = ProductView(parent)
        self._view.controller = self
        self.initialize()
    
    def initialize(self):
        """Initialize the controller"""
        self.refresh_view()
        self._update_categories()
        self._update_suppliers()
    
    def refresh_view(self):
        """Refresh the view with current data"""
        try:
            products = self._model.get_all()
            self._view.refresh(products)
        except Exception as e:
            self.handle_error(e, "refreshing products")
    
    def _update_categories(self):
        """Update category list in view"""
        try:
            categories = self._category_model.get_all()
            self._view.update_categories(categories)
        except Exception as e:
            self.handle_error(e, "loading categories")
    
    def _update_suppliers(self):
        """Update supplier list in view"""
        try:
            suppliers = self._supplier_model.get_all()
            self._view.update_suppliers(suppliers)
        except Exception as e:
            self.handle_error(e, "loading suppliers")
    
    def add_product(self, name: str, description: str, price: float,
                   category_id: int = None, supplier_id: int = None):
        """Add a new product"""
        try:
            if not name:
                raise ValueError("Product name is required")
            if price <= 0:
                raise ValueError("Price must be greater than 0")
                
            self._model.add(name, description, price, category_id, supplier_id)
            self._view.show_success("Product added successfully")
            self.refresh_view()
            self._view._on_clear()
            
        except Exception as e:
            self.handle_error(e, "adding product")
    
    def update_product(self, product_id: int, name: str, description: str,
                      price: float, category_id: int = None, supplier_id: int = None):
        """Update an existing product"""
        try:
            if not name:
                raise ValueError("Product name is required")
            if price <= 0:
                raise ValueError("Price must be greater than 0")
                
            self._model.update(product_id, name, description, price, category_id, supplier_id)
            self._view.show_success("Product updated successfully")
            self.refresh_view()
            
        except Exception as e:
            self.handle_error(e, "updating product")
    
    def delete_product(self, product_id: int):
        """Delete a product"""
        try:
            self._model.delete(product_id)
            self._view.show_success("Product deleted successfully")
            self.refresh_view()
            self._view._on_clear()
            
        except Exception as e:
            self.handle_error(e, "deleting product")
