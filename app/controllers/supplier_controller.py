from app.models.supplier_model import SupplierModel

class SupplierController:
    def __init__(self):
        self.model = SupplierModel()

    def layTatCaNhaCungCap(self):
        """Get all suppliers"""
        try:
            return self.model.layTatCa()
        except Exception as e:
            self.handle_error(e, "lấy tất cả nhà cung cấp")
            return []

    def themNhaCungCap(self, data):
        """Add a new supplier"""
        try:
            if not data.get('ten'):
                raise ValueError("Tên nhà cung cấp là bắt buộc")
            return self.model.them(**data)
        except Exception as e:
            self.handle_error(e, "thêm nhà cung cấp")
            raise

    def capNhatNhaCungCap(self, data):
        """Update an existing supplier"""

        try:
            if not data.get('ma_ncc'):
                raise ValueError("Mã nhà cung cấp là bắt buộc")
            if not data.get('ten'):
                raise ValueError("Tên nhà cung cấp là bắt buộc")
            return self.model.capNhat(data)
        except Exception as e:
            self.handle_error(e, "cập nhật nhà cung cấp")
            raise

    def xoaNhaCungCap(self, ma_ncc):
        """Delete a supplier"""
        try:
            if not ma_ncc:
                raise ValueError("Mã nhà cung cấp là bắt buộc")
            return self.model.xoa(ma_ncc)
        except Exception as e:
            self.handle_error(e, "xóa nhà cung cấp")
            raise

    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)
        return error_message

    def layNhaCungCapPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", contact_sort="none"):
        """Get paginated suppliers with optional search and sorting"""
        try:
            return self.model.layNhaCungCapPhanTrang(
                offset=offset,
                limit=limit,
                search_query=search_query,
                name_sort=name_sort,
                contact_sort=contact_sort
            )
        except Exception as e:
            self.handle_error(e, "lấy danh sách nhà cung cấp phân trang")
            return [], 0

    def lay_nha_cung_cap_theo_id(self, ma_ncc):
        """Get a supplier by ID"""
        try:
            if not ma_ncc:
                raise ValueError("ID nhà cung cấp là bắt buộc")
            return self.model.layTheoId(ma_ncc)
        except Exception as e:
            self.handle_error(e, "lấy nhà cung cấp theo ID")
            raise



