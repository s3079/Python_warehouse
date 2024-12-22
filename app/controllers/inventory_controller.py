from app.controllers.base_controller import BaseController
from app.models.inventory_model import InventoryModel
from app.models.product_model import ProductModel
from app.views.inventory_view import InventoryView

class InventoryController(BaseController):
    def __init__(self, parent):
        super().__init__()
        self._model = InventoryModel()
        self._product_model = ProductModel()
        self._view = InventoryView(parent)
        self._view.controller = self
        self.initialize()
    
    def initialize(self):
        """Initialize the controller"""
        self.refresh_view()
        self._update_products()
    
    def refresh_view(self):
        """Refresh the view with current data"""
        try:
            inventory = self._model.get_all()
            self._view.refresh(inventory)
        except Exception as e:
            self.handle_error(e, "refreshing inventory")
    
    def _update_products(self):
        """Update product list in view"""
        try:
            products = self._product_model.get_all()
            self._view.update_products(products)
        except Exception as e:
            self.handle_error(e, "loading products")
    
    def update_inventory(self, product_id: int, quantity: int):
        """Update inventory quantity"""
        try:
            if product_id is None:
                raise ValueError("Please select a product")
                
            self._model.update_quantity(product_id, quantity)
            self._view.show_success("Inventory updated successfully")
            self.refresh_view()
            self._view._on_clear()
            
        except Exception as e:
            self.handle_error(e, "updating inventory")
    
    def show_low_stock(self, threshold: int = 10):
        """Show low stock items"""
        try:
            low_stock = self._model.get_low_stock_items(threshold)
            self._view.refresh(low_stock)
            if not low_stock:
                self._view.show_success("No low stock items found")
        except Exception as e:
            self.handle_error(e, "checking low stock")
