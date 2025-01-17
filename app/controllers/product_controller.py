from app.models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self._model = ProductModel()
    
    def layTatCaSanPham(self):
        """Get all products with their category and supplier names"""
        try:
            san_pham = self._model.layTatCa()
            print("san_pham", san_pham)
            if not san_pham:
                return []
            
            # Results are already in dictionary format from the model
            formatted_products = []
            for product in san_pham:
                product_dict = {
                    "ma_san_pham": product["ma_san_pham"],
                    "ten": product["ten"],
                    "mo_ta": product["mo_ta"] if product["mo_ta"] else "",
                    "don_gia": product["don_gia"],
                    "ma_danh_muc": product["ma_danh_muc"],
                    "ma_ncc": product["ma_ncc"],
                    "ngay_tao": product["ngay_tao"],
                    "ngay_cap_nhat": product["ngay_cap_nhat"],
                    "ten_danh_muc": product["ten_danh_muc"] if product["ten_danh_muc"] else "",
                    "ten_ncc": product["ten_nha_cung_cap"] if product["ten_nha_cung_cap"] else ""
                }
                formatted_products.append(product_dict)
            return formatted_products
        except Exception as e:
            self.handle_error(e, "lấy tất cả sản phẩm")
            return []
    
    def themSanPham(self, data):
        """Add a new product"""
        try:
            if not data.get('ten'):
                raise ValueError("Tên sản phẩm là bắt buộc")
            return self._model.them(**data)
        except Exception as e:
            self.handle_error(e, "thêm sản phẩm")
            raise
    
    def capNhatSanPham(self, ma_san_pham, data):
        """Update an existing product"""
        try:
            if not ma_san_pham:
                raise ValueError("Mã sản phẩm là bắt buộc")
            if not data.get('ten'):
                raise ValueError("Tên sản phẩm là bắt buộc")
            return self._model.capNhat(ma_san_pham=ma_san_pham, **data)
        except Exception as e:
            self.handle_error(e, "cập nhật sản phẩm")
            raise
    
    def xoaSanPham(self, ma_san_pham):
        """Delete a product"""
        try:
            if not ma_san_pham:
                raise ValueError("Mã sản phẩm là bắt buộc")
            return self._model.xoa(ma_san_pham)
        except Exception as e:
            self.handle_error(e, "xóa sản phẩm")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message
    
    def laySanPhamPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", price_sort="none"):
        """Get paginated products with optional search and sorting"""
        try:
            filters = {}
            if name_sort and name_sort != "none":
                filters['name_sort'] = name_sort.upper()
            if price_sort and price_sort != "none":
                filters['price_sort'] = price_sort.upper()
            
            return self._model.laySanPhamPhanTrang(offset, limit, search_query, filters)
        except Exception as e:
            self.handle_error(e, "lấy danh sách sản phẩm phân trang")
            return [], 0