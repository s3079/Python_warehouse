from app.controllers.base_controller import BaseController
from app.models.supplier_model import SupplierModel
from app.views.supplier_view import SupplierView

class SupplierController(BaseController):
    def __init__(self, parent):
        super().__init__()
        self._model = SupplierModel()
        self._view = SupplierView(parent)
        self._view.controller = self
        self.initialize()
    
    def initialize(self):
        """Initialize the controller"""
        self.refresh_view()
    
    def refresh_view(self):
        """Refresh the view with current data"""
        try:
            suppliers = self._model.get_all()
            self._view.refresh(suppliers)
        except Exception as e:
            self.handle_error(e, "refreshing suppliers")
    
    def add_supplier(self, name: str, contact_name: str = None, 
                    address: str = None, phone: str = None, email: str = None):
        """Add a new supplier"""
        try:
            if not name:
                raise ValueError("Supplier name is required")
                
            self._model.add(name, contact_name, address, phone, email)
            self._view.show_success("Supplier added successfully")
            self.refresh_view()
            self._view._on_clear()  # Clear form after successful add
            
        except Exception as e:
            self.handle_error(e, "adding supplier")
    
    def update_supplier(self, supplier_id: int, name: str, contact_name: str = None, 
                       address: str = None, phone: str = None, email: str = None):
        """Update an existing supplier"""
        try:
            if not name:
                raise ValueError("Supplier name is required")
                
            self._model.update(supplier_id, name, contact_name, address, phone, email)
            self._view.show_success("Supplier updated successfully")
            self.refresh_view()
            
        except Exception as e:
            self.handle_error(e, "updating supplier")
    
    def delete_supplier(self, supplier_id: int):
        """Delete a supplier"""
        try:
            self._model.delete(supplier_id)
            self._view.show_success("Supplier deleted successfully")
            self.refresh_view()
            self._view._on_clear()  # Clear form after successful delete
            
        except Exception as e:
            self.handle_error(e, "deleting supplier")
