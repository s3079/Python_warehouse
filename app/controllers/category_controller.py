from app.models.category_model import CategoryModel

class CategoryController:
    def __init__(self):
        self._model = CategoryModel()
    
    def layTatCaDanhMuc(self, name_sort="none", desc_sort="none", ten_filter=None):
        """
        + Input:
            - name_sort: Hướng sắp xếp theo tên ('asc', 'desc', 'none') (mặc định: "none")
            - desc_sort: Hướng sắp xếp theo mô tả ('asc', 'desc', 'none') (mặc định: "none")
            - ten_filter: Từ khóa lọc theo tên danh mục (mặc định: None)
        + Output: Danh sách các từ điển chứa thông tin danh mục:
            - ma_danh_muc: Mã danh mục
            - ten: Tên danh mục
            - mo_ta: Mô tả danh mục
            - ngay_tao: Ngày tạo
            - ngay_cap_nhat: Ngày cập nhật
            - tong_san_pham: Số lượng sản phẩm trong danh mục
        """
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
        """
        + Input:
            - ten: Tên danh mục (bắt buộc)
            - mo_ta: Mô tả danh mục (mặc định: "")
        + Output: Thông tin danh mục vừa được tạo
        + Raises:
            - ValueError khi thiếu tên danh mục
            - Exception khi thêm danh mục thất bại
        """
        try:
            if not ten:
                raise ValueError("Tên danh mục là bắt buộc")
            return self._model.them(ten, mo_ta)
        except Exception as e:
            self.handle_error(e, "thêm danh mục")
            raise
    
    def capNhat(self, ma_danh_muc, ten, mo_ta=""):
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần cập nhật (bắt buộc)
            - ten: Tên danh mục mới (bắt buộc)
            - mo_ta: Mô tả danh mục mới (mặc định: "")
        + Output: Thông tin danh mục sau khi cập nhật
        + Raises:
            - ValueError khi thiếu mã danh mục hoặc tên danh mục
            - Exception khi cập nhật danh mục thất bại
        """
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
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần xóa
        + Output: Kết quả xóa danh mục
        + Raises:
            - ValueError khi:
                + Thiếu mã danh mục
                + Danh mục đang chứa sản phẩm
            - Exception khi xóa danh mục thất bại
        """
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
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần tìm
        + Output: Thông tin của danh mục
        + Raises:
            - ValueError khi thiếu mã danh mục
            - Exception khi lấy thông tin danh mục thất bại
        """
        try:
            if not ma_danh_muc:
                raise ValueError("ID danh mục là bắt buộc")
            return self._model.layTheoId(ma_danh_muc)
        except Exception as e:
            self.handle_error(e, "lấy danh mục theo ID")
            raise
    
    def handle_error(self, error, action):
        """
        + Input:
            - error: Đối tượng lỗi
            - action: Chuỗi mô tả hành động đang thực hiện
        + Output: Chuỗi thông báo lỗi đã được định dạng
        """
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)
        return error_message

