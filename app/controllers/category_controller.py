from app.models.category_model import CategoryModel

class CategoryController:
    def __init__(self):
        self._model = CategoryModel()
    
    def get_all_categories(self):
        """Get all categories with their product counts""" 
        try:
            categories = self._model.get_all()
            if not categories:
                return []
                
            # Results are already in dictionary format
            formatted_categories = []
            for category in categories:
                category_dict = {
                    "category_id": category["category_id"],
                    "name": category["name"],
                    "description": category["description"] if category["description"] else "",
                    "created_at": category["created_at"],
                    "updated_at": category["updated_at"],
                    "total_products": self._model.count_products(category["category_id"])
                }
                formatted_categories.append(category_dict)
            return formatted_categories
        except Exception as e:
            print(f"Lỗi khi lấy danh mục: {e}")
            self.handle_error(e, "lấy danh mục")
            return []
    
    def add(self, name, description=""):
        """Add a new category"""
        try:
            if not name:
                raise ValueError("Tên danh mục là bắt buộc")
            return self._model.add(name, description)
        except Exception as e:
            self.handle_error(e, "thêm danh mục")
            raise
    
    def update(self, category_id, name, description=""):
        """Update an existing category"""
        try:
            if not category_id:
                raise ValueError("ID danh mục là bắt buộc")
            if not name:
                raise ValueError("Tên danh mục là bắt buộc")
            return self._model.update(category_id, name, description)
        except Exception as e:
            self.handle_error(e, "cập nhật danh mục")
            raise
    
    def delete(self, category_id):
        """Delete a category"""
        try:
            if not category_id:
                raise ValueError("ID danh mục là bắt buộc")
                
            # Check if category has products
            product_count = self._model.count_products(category_id)
            if product_count > 0:
                raise ValueError(f"Không thể xóa danh mục có {product_count} sản phẩm")
                
            return self._model.delete(category_id)
        except Exception as e:
            self.handle_error(e, "xóa danh mục")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message
