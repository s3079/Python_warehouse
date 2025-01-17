from app.models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self._model = ProductModel()
    
    def layTatCaSanPham(self):
        """
        + Input: Không có
        + Output: Danh sách các từ điển chứa thông tin sản phẩm:
            - ma_san_pham: Mã sản phẩm
            - ten: Tên sản phẩm
            - mo_ta: Mô tả sản phẩm
            - don_gia: Đơn giá
            - ma_danh_muc: Mã danh mục
            - ma_ncc: Mã nhà cung cấp
            - ngay_tao: Ngày tạo
            - ngay_cap_nhat: Ngày cập nhật
            - ten_danh_muc: Tên danh mục
            - ten_ncc: Tên nhà cung cấp
        """
        try:
            san_pham = self._model.layTatCa()
            if not san_pham:
                return []

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
        """
        + Input:
            - data (từ điển): Dữ liệu sản phẩm bao gồm:
                + ten: Tên sản phẩm (bắt buộc)
                + mo_ta: Mô tả sản phẩm
                + don_gia: Đơn giá
                + ma_danh_muc: Mã danh mục
                + ma_ncc: Mã nhà cung cấp
        + Output: Từ điển chứa thông tin sản phẩm vừa tạo
        + Raises:
            - ValueError khi thiếu tên sản phẩm
            - Exception khi thêm sản phẩm thất bại
        """
        try:
            if not data.get('ten'):
                raise ValueError("Tên sản phẩm là bắt buộc")
            return self._model.them(**data)
        except Exception as e:
            self.handle_error(e, "thêm sản phẩm")
            raise
    
    def capNhatSanPham(self, ma_san_pham, data):
        """
        + Input:
            - ma_san_pham: Mã sản phẩm cần cập nhật
            - data (từ điển): Dữ liệu sản phẩm cập nhật bao gồm:
                + ten: Tên sản phẩm (bắt buộc)
                + mo_ta: Mô tả sản phẩm
                + don_gia: Đơn giá
                + ma_danh_muc: Mã danh mục
                + ma_ncc: Mã nhà cung cấp
        + Output: Từ điển chứa thông tin sản phẩm sau khi cập nhật
        + Raises:
            - ValueError khi thiếu mã sản phẩm hoặc tên sản phẩm
            - Exception khi cập nhật thất bại
        """
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
        """
        + Input:
            - ma_san_pham: Mã sản phẩm cần xóa
        + Output: Giá trị boolean thể hiện việc xóa thành công hay không
        + Raises:
            - ValueError khi thiếu mã sản phẩm
            - Exception khi xóa thất bại
        """
        try:
            if not ma_san_pham:
                raise ValueError("Mã sản phẩm là bắt buộc")
            return self._model.xoa(ma_san_pham)
        except Exception as e:
            self.handle_error(e, "xóa sản phẩm")
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
    
    def laySanPhamPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", price_sort="none"):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm sản phẩm (mặc định: "")
            - name_sort: Hướng sắp xếp theo tên ('asc', 'desc', 'none') (mặc định: "none")
            - price_sort: Hướng sắp xếp theo giá ('asc', 'desc', 'none') (mặc định: "none")
        + Output: Tuple chứa:
            - Danh sách các từ điển thông tin sản phẩm thỏa mãn điều kiện
            - Tổng số sản phẩm thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi lấy dữ liệu thất bại
        """
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