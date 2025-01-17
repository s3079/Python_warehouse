from app.models.order_model import OrderModel

class OrderController:
    def __init__(self):
        self._model = OrderModel()
    
    def layDonHangPhanTrang(self, offset=0, limit=10):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
        + Output: Tuple chứa:
            - Danh sách các từ điển thông tin đơn hàng thỏa mãn điều kiện
            - Tổng số đơn hàng thỏa mãn điều kiện
        + Raises:
            - Exception khi lấy dữ liệu thất bại
        """
        try:
            return self._model.layDonHangPhanTrang(offset, limit)
        except Exception as e:
            self.handle_error(e, "lấy danh sách đơn hàng phân trang")
            return [], 0
    
    def capNhatDonHang(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu đơn hàng cập nhật bao gồm:
                + ma_don_hang: Mã đơn hàng (bắt buộc)
                + ngay_dat: Ngày đặt hàng (bắt buộc)
                + so_luong: Số lượng (bắt buộc)
                + tong_tien: Tổng tiền (bắt buộc)
                + ma_san_pham: Mã sản phẩm (bắt buộc)
                + ma_nguoi_dung: Mã người dùng
                + don_gia: Đơn giá
        + Output: True nếu cập nhật thành công, False nếu thất bại
        + Raises:
            - ValueError khi thiếu thông tin bắt buộc
            - Exception khi cập nhật đơn hàng thất bại
        """
        try:
            # Validate data
            required_fields = ['ma_don_hang', 'ngay_dat', 'so_luong', 'tong_tien', 'ma_san_pham']
            if not all(key in data for key in required_fields):
                raise ValueError("Thiếu thông tin bắt buộc")

            return self._model.capNhatDonHang(
                ma_don_hang=data['ma_don_hang'],
                ngay_dat=data['ngay_dat'],
                so_luong=data['so_luong'],
                tong_tien=data['tong_tien'],
                ma_san_pham=data['ma_san_pham'],
                ma_nguoi_dung=data['ma_nguoi_dung'],
                don_gia=data['don_gia']
            )
        except Exception as e:
            print(f"Lỗi trong controller capNhatDonHang: {e}")
            return False
    
    def xoaDonHang(self, ma_don_hang):
        """
        + Input:
            - ma_don_hang: Mã đơn hàng cần xóa
        + Output: True nếu xóa thành công, False nếu thất bại
        + Raises:
            - ValueError khi thiếu mã đơn hàng
            - Exception khi xóa đơn hàng thất bại
        """
        try:
            if not ma_don_hang:
                raise ValueError("Mã đơn hàng là bắt buộc")
            return self._model.xoa(ma_don_hang)
        except Exception as e:
            self.handle_error(e, "xóa đơn hàng")
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
    
    def layChiTietDonHang(self, ma_don_hang):
        """
        + Input:
            - ma_don_hang: Mã đơn hàng cần lấy chi tiết
        + Output: Từ điển chứa thông tin chi tiết đơn hàng hoặc None nếu không tìm thấy
        + Raises:
            - Exception khi lấy chi tiết đơn hàng thất bại
        """
        try:
            print('ma_don_hang', ma_don_hang)
            return self._model.layChiTietDonHang(ma_don_hang)
        except Exception as e:
            self.handle_error(e, "lấy chi tiết đơn hàng")
            return None 
    
    def themDonHang(self, data):
        """
        + Input:
            - data (từ điển): Dữ liệu đơn hàng mới bao gồm:
                + ngay_dat: Ngày đặt hàng
                + tong_tien: Tổng tiền
                + ma_san_pham: Mã sản phẩm
                + so_luong: Số lượng
                + don_gia: Đơn giá
                + ma_nguoi_dung: Mã người dùng
        + Output: True nếu thêm thành công, False nếu thất bại
        + Raises:
            - ValueError khi thêm đơn hàng thất bại
            - Exception khi thêm đơn hàng hoặc chi tiết đơn hàng thất bại
        """
        try:
            ngay_dat = data.get("ngay_dat")
            tong_tien = data.get("tong_tien")
            ma_san_pham = data.get("ma_san_pham")
            so_luong = data.get("so_luong")
            don_gia = data.get("don_gia")
            ma_nguoi_dung = data.get("ma_nguoi_dung")
            
            # Add order and get order_id
            ma_don_hang = self._model.them(ngay_dat, tong_tien, ma_nguoi_dung)
            
            if ma_don_hang:
                self._model.themChiTietDonHang(ma_don_hang, ma_san_pham, so_luong, don_gia)
            else:
                raise ValueError("Thêm đơn hàng thất bại")
            
            return ma_don_hang is not None
        except Exception as e:
            self.handle_error(e, "thêm đơn hàng")
            raise

    def layMaSanPhamTheoTen(self, ten_san_pham):
        """
        + Input:
            - ten_san_pham: Tên sản phẩm cần tìm
        + Output: Mã sản phẩm tương ứng hoặc None nếu không tìm thấy
        + Raises:
            - Exception khi lấy mã sản phẩm thất bại
        """
        try:
            return self._model.layMaSanPhamTheoTen(ten_san_pham)
        except Exception as e:
            self.handle_error(e, "lấy mã sản phẩm theo tên")
            return None 