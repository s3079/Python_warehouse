from app.models.inventory_model import InventoryModel
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel

class InventoryController:
    def __init__(self):
        self._model = InventoryModel()
        self._category_model = CategoryModel()
        self._product_model = ProductModel()
    
    def layTatCaKhoHang(self):
        """
        + Input: Không có
        + Output: Danh sách các từ điển chứa thông tin kho hàng:
            - ma_kho: Mã kho hàng
            - ten_san_pham: Tên sản phẩm
            - so_luong: Số lượng tồn kho
        """
        try:
            kho_hang = self._model.layTatCa()
            if not kho_hang:
                return []
            
            formatted_inventory = []
            for item in kho_hang:
                item_dict = {
                    "ma_kho": item["ma_kho"],
                    "ten_san_pham": item["ten_san_pham"],
                    "so_luong": item["so_luong"]
                }
                formatted_inventory.append(item_dict)
            return formatted_inventory
        except Exception as e:
            self.handle_error(e, "lấy tất cả kho hàng")
            return []
    
    def themKhoHang(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu kho hàng bao gồm:
                + ma_san_pham: Mã sản phẩm (bắt buộc)
                + so_luong: Số lượng
                + ngay_nhap_cuoi: Ngày nhập kho cuối cùng
        + Output: Thông tin kho hàng vừa được tạo
        + Raises:
            - ValueError khi thiếu mã sản phẩm
            - Exception khi thêm kho hàng thất bại
        """
        try:
            if 'ma_san_pham' not in data:
                raise ValueError("Mã sản phẩm là bắt buộc")
            return self._model.them(**data)
        except Exception as e:
            self.handle_error(e, "thêm kho hàng")
            raise
    
    def capNhatKhoHang(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu cập nhật kho hàng:
                + ma_kho: Mã kho hàng (bắt buộc)
                + ma_san_pham: Mã sản phẩm (bắt buộc)
                + so_luong: Số lượng (bắt buộc)
                + ngay_nhap_cuoi: Ngày nhập kho cuối cùng (bắt buộc)
        + Output: Thông tin kho hàng sau khi cập nhật
        + Raises:
            - ValueError khi thiếu một trong các trường bắt buộc
            - Exception khi cập nhật kho hàng thất bại
        """
        try:
            if not data.get('ma_kho'):
                raise ValueError("Mã kho là bắt buộc")
            if not data.get('ma_san_pham'):
                raise ValueError("Mã sản phẩm là bắt buộc")
            if not data.get('so_luong'):
                raise ValueError("Số lượng là bắt buộc")
            if not data.get('ngay_nhap_cuoi'):
                raise ValueError("Ngày nhập kho là bắt buộc")

            data = {
                "ma_kho": data.get('ma_kho'),
                "ma_san_pham": data.get('ma_san_pham'),
                "so_luong": data.get('so_luong'),
                "ngay_nhap_cuoi": data.get('ngay_nhap_cuoi')
            }
            
            return self._model.capNhat(data)
        except Exception as e:
            self.handle_error(e, "cập nhật kho hàng")
            raise
    
    def xoaKhoHang(self, ma_kho):
        """
        + Input:
            - ma_kho: Mã kho hàng cần xóa
        + Output: Kết quả xóa kho hàng
        + Raises:
            - ValueError khi thiếu mã kho hàng
            - Exception khi xóa kho hàng thất bại
        """
        try:
            if not ma_kho:
                raise ValueError("Mã kho là bắt buộc")
            return self._model.xoa(ma_kho)
        except Exception as e:
            self.handle_error(e, "xóa kho hàng")
            raise
    
    def handle_error(self, error, action):
        """
        + Input:
            - error: Đối tượng lỗi
            - action: Chuỗi mô tả hành động đang thực hiện
        + Output: Chuỗi thông báo lỗi đã được định dạng
        """
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message
    
    def layKhoHangPhanTrang(self, offset=0, limit=10, search_query=""):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm kho hàng (mặc định: "")
        + Output: Tuple chứa:
            - Danh sách các từ điển thông tin kho hàng thỏa mãn điều kiện
            - Tổng số kho hàng thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi lấy dữ liệu thất bại
        """
        try:
            return self._model.layKhoHangPhanTrang(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "lấy danh sách kho hàng phân trang")
            return [], 0
    
    def layTenDanhMuc(self):
        """
        + Input: Không có
        + Output: Danh sách tên các danh mục
        + Raises:
            - Exception khi lấy danh sách danh mục thất bại
        """
        try:
            danh_muc = self._category_model.layTatCaDanhMuc()
            return [category['ten'] for category in danh_muc]
        except Exception as e:
            self.handle_error(e, "lấy tên danh mục")
            return []
    
    def layTenSanPham(self):
        """
        + Input: Không có
        + Output: Danh sách tên các sản phẩm
        + Raises:
            - Exception khi lấy danh sách sản phẩm thất bại
        """
        try:
            san_pham = self._product_model.layTatCaSanPham()
            return [product['ten'] for product in san_pham]
        except Exception as e:
            self.handle_error(e, "lấy tên sản phẩm")
            return []
    
    def layMaSanPhamTheoTen(self, ten_san_pham):
        """
        + Input:
            - ten_san_pham: Tên sản phẩm cần tìm
        + Output: Mã sản phẩm tương ứng hoặc None nếu không tìm thấy
        + Raises:
            - Exception khi lấy mã sản phẩm thất bại
        """
        try:
            san_pham = self._product_model.layTheoTen(ten_san_pham)
            return san_pham['ma_san_pham'] if san_pham else None
        except Exception as e:
            self.handle_error(e, "lấy mã sản phẩm theo tên")
            return None