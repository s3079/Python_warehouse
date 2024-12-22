from app.controllers.base_controller import BaseController
from app.models.category_model import CategoryModel
from app.views.category_view import CategoryView

class CategoryController(BaseController):
    def __init__(self, parent):
        super().__init__()
        self._model = CategoryModel()
        self._view = CategoryView(parent)
        self._view.controller = self
        self.initialize()
    
    def initialize(self):
        """Initialize the controller"""
        self.refresh_view()
    
    def refresh_view(self):
        """Refresh the view with current data"""
        try:
            categories = self._model.get_all()
            self._view.refresh(categories)
        except Exception as e:
            self.handle_error(e, "refreshing categories")
    
    def add_category(self, name: str, description: str):
        """Add a new category"""
        try:
            if not name:
                raise ValueError("Category name is required")
                
            self._model.add(name, description)
            self._view.show_success("Category added successfully")
            self.refresh_view()
            
        except Exception as e:
            self.handle_error(e, "adding category")
    
    def update_category(self, category_id: int, name: str, description: str):
        """Update an existing category"""
        try:
            if not name:
                raise ValueError("Category name is required")
                
            self._model.update(category_id, name, description)
            self._view.show_success("Category updated successfully")
            self.refresh_view()
            
        except Exception as e:
            self.handle_error(e, "updating category")
    
    def delete_category(self, category_id: int):
        """Delete a category"""
        try:
            self._model.delete(category_id)
            self._view.show_success("Category deleted successfully")
            self.refresh_view()
            
        except Exception as e:
            self.handle_error(e, "deleting category")
