from app.models.supplier_model import SupplierModel

class SupplierController:
    def __init__(self):
        self.model = SupplierModel()

    def layTatCaNhaCungCap(self):
        """
        + Input: Không có
        + Output: Danh sách các từ điển chứa thông tin nhà cung cấp:
            - ma_ncc: Mã nhà cung cấp
            - ten: Tên nhà cung cấp
            - dia_chi: Địa chỉ
            - email: Email
            - so_dien_thoai: Số điện thoại
            - ngay_tao: Ngày tạo
            - ngay_cap_nhat: Ngày cập nhật
        """
        try:
            return self.model.layTatCa()
        except Exception as e:
            self.handle_error(e, "lấy tất cả nhà cung cấp")
            return []

    def themNhaCungCap(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu nhà cung cấp bao gồm:
                + ten: Tên nhà cung cấp (bắt buộc)
                + dia_chi: Địa chỉ
                + email: Email
                + so_dien_thoai: Số điện thoại
        + Output: Thông tin nhà cung cấp vừa được tạo
        + Raises:
            - ValueError khi thiếu tên nhà cung cấp
            - Exception khi thêm nhà cung cấp thất bại
        """
        try:
            if not data.get('ten'):
                raise ValueError("Tên nhà cung cấp là bắt buộc")
            return self.model.them(**data)
        except Exception as e:
            self.handle_error(e, "thêm nhà cung cấp")
            raise

    def capNhatNhaCungCap(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu cập nhật nhà cung cấp:
                + ma_ncc: Mã nhà cung cấp (bắt buộc)
                + ten: Tên nhà cung cấp (bắt buộc)
                + dia_chi: Địa chỉ
                + email: Email
                + so_dien_thoai: Số điện thoại
        + Output: Thông tin nhà cung cấp sau khi cập nhật
        + Raises:
            - ValueError khi thiếu mã hoặc tên nhà cung cấp
            - Exception khi cập nhật nhà cung cấp thất bại
        """
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
        """
        + Input:
            - ma_ncc: Mã nhà cung cấp cần xóa
        + Output: True nếu xóa thành công, False nếu thất bại
        + Raises:
            - ValueError khi thiếu mã nhà cung cấp
            - Exception khi xóa nhà cung cấp thất bại
        """
        try:
            if not ma_ncc:
                raise ValueError("Mã nhà cung cấp là bắt buộc")
            return self.model.xoa(ma_ncc)
        except Exception as e:
            self.handle_error(e, "xóa nhà cung cấp")
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

    def layNhaCungCapPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", contact_sort="none"):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm nhà cung cấp (mặc định: "")
            - name_sort: Hướng sắp xếp theo tên ('asc', 'desc', 'none') (mặc định: "none")
            - contact_sort: Hướng sắp xếp theo liên hệ ('asc', 'desc', 'none') (mặc định: "none")
        + Output: Tuple chứa:
            - Danh sách các từ điển thông tin nhà cung cấp thỏa mãn điều kiện
            - Tổng số nhà cung cấp thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi lấy dữ liệu thất bại
        """
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
        """
        + Input:
            - ma_ncc: Mã nhà cung cấp cần tìm
        + Output: Thông tin của nhà cung cấp hoặc None nếu không tìm thấy
        + Raises:
            - ValueError khi thiếu mã nhà cung cấp
            - Exception khi lấy thông tin nhà cung cấp thất bại
        """
        try:
            if not ma_ncc:
                raise ValueError("ID nhà cung cấp là bắt buộc")
            return self.model.layTheoId(ma_ncc)
        except Exception as e:
            self.handle_error(e, "lấy nhà cung cấp theo ID")
            raise



