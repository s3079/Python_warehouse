from app.models.category_model import CategoryModel

class CategoryController:
    def __init__(self):
        self._model = CategoryModel()
    
    def layTatCaDanhMuc(self, name_sort="none", desc_sort="none", ten_filter=None):
        try:
            categories = self._model.layTatCa(name_sort, desc_sort)
            if not categories:
                return []
                
            formatted_categories = []
            for category in categories:
                if ten_filter and ten_filter.lower() not in category["ten"].lower():
                    continue
                    
                category_dict = {
                    "ma_danh_muc": category["ma_danh_muc"],
                    "ten": category["ten"],
                    "mo_ta": category["mo_ta"] if category["mo_ta"] else "",
                    "ngay_tao": category["ngay_tao"],
                    "ngay_cap_nhat": category["ngay_cap_nhat"],
                    "tong_san_pham": self._model.demSanPham(category["ma_danh_muc"])
                }
                formatted_categories.append(category_dict)
            return formatted_categories
        except Exception as e:
            self.handle_error(e, "lấy danh mục")
            return []
    
    def them(self, ten, mo_ta=""):
        try:
            if not ten:
                raise ValueError("Tên danh mục là bắt buộc")
            return self._model.them(ten, mo_ta)
        except Exception as e:
            self.handle_error(e, "thêm danh mục")
            raise
    
    def capNhat(self, ma_danh_muc, ten, mo_ta=""):
        try:
            if not ma_danh_muc:
                raise ValueError("ID danh mục là bắt buộc")
            if not ten:
                raise ValueError("Tên danh mục là bắt buộc")
            return self._model.capNhat(ma_danh_muc, ten, mo_ta)
        except Exception as e:
            self.handle_error(e, "cập nhật danh mục")
            raise
    
    def xoa(self, ma_danh_muc):
        try:
            if not ma_danh_muc:
                raise ValueError("ID danh mục là bắt buộc")
                
            product_count = self._model.demSanPham(ma_danh_muc)
            if product_count > 0:
                raise ValueError(f"Không thể xóa danh mục có {product_count} sản phẩm")
                
            return self._model.xoa(ma_danh_muc)
        except Exception as e:
            self.handle_error(e, "xóa danh mục")
            raise

    def lay_danh_muc_theo_id(self, ma_danh_muc):
        try:
            if not ma_danh_muc:
                raise ValueError("ID danh mục là bắt buộc")
            return self._model.layTheoId(ma_danh_muc)
        except Exception as e:
            self.handle_error(e, "lấy danh mục theo ID")
            raise
    
    def handle_error(self, error, action):
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)
        return error_message

