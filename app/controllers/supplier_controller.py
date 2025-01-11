from app.models.supplier_model import SupplierModel

class SupplierController:
    def __init__(self):
        self.model = SupplierModel()

    def get_all_suppliers(self):
        """Retrieve all suppliers"""
        try:
            return self.model.get_all()
        except Exception as e:
            raise Exception(f"Failed to retrieve suppliers: {str(e)}")

    def add_supplier(self, name, contact_name=None, address=None, phone=None, email=None):
        """Add a new supplier"""
        try:
            return self.model.add(name, contact_name, address, phone, email)
        except Exception as e:
            raise Exception(f"Failed to add supplier: {str(e)}")

    def update_supplier(self, supplier_id, name, contact_name=None, address=None, phone=None, email=None):
        """Update an existing supplier"""
        try:
            return self.model.update(supplier_id, name, contact_name, address, phone, email)
        except Exception as e:
            raise Exception(f"Failed to update supplier: {str(e)}")

    def delete_supplier(self, supplier_id):
        """Delete a supplier"""
        try:
            return self.model.delete(supplier_id)
        except Exception as e:
            raise Exception(f"Failed to delete supplier: {str(e)}")

    def get_supplier_by_id(self, supplier_id):
        """Get a supplier by ID"""
        try:
            return self.model.get_by_id(supplier_id)
        except Exception as e:
            raise Exception(f"Failed to retrieve supplier: {str(e)}") 