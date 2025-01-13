from app.models.supplier_model import SupplierModel

class SupplierController:
    def __init__(self):
        self.model = SupplierModel()

    def get_all_suppliers(self):
        """Get all suppliers"""
        try:
            return self.model.get_all()
        except Exception as e:
            self.handle_error(e, "getting all suppliers")
            return []

    def add_supplier(self, data):
        """Add a new supplier"""
        try:
            if not data.get('name'):
                raise ValueError("Supplier name is required")
            return self.model.add(**data)
        except Exception as e:
            self.handle_error(e, "adding supplier")
            raise

    def update_supplier(self, supplier_id, data):
        """Update an existing supplier"""
        try:
            if not supplier_id:
                raise ValueError("Supplier ID is required")
            if not data.get('name'):
                raise ValueError("Supplier name is required")
            return self.model.update(supplier_id=supplier_id, **data)
        except Exception as e:
            self.handle_error(e, "updating supplier")
            raise

    def delete_supplier(self, supplier_id):
        """Delete a supplier"""
        try:
            if not supplier_id:
                raise ValueError("Supplier ID is required")
            return self.model.delete(supplier_id)
        except Exception as e:
            self.handle_error(e, "deleting supplier")
            raise

    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Error {action}: {str(error)}"
        print(error_message)
        return error_message

    def get_suppliers_paginated(self, offset=0, limit=10, search_query=""):
        """Get paginated suppliers with optional search"""
        try:
            return self.model.get_suppliers_paginated(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "getting paginated suppliers")
            return [], 0

