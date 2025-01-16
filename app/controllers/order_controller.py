from app.models.order_model import OrderModel

class OrderController:
    def __init__(self):
        self._model = OrderModel()
    
    def layDonHangPhanTrang(self, offset=0, limit=10, search_query=""):
        """Get paginated orders with optional search"""
        try:
            return self._model.layDonHangPhanTrang(offset, limit, search_query)
        except Exception as e:
            self.handle_error(e, "lấy danh sách đơn hàng phân trang")
            return [], 0
    
    def capNhatDonHang(self, data):
        """Update an existing order"""
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
        """Delete an order"""
        try:
            if not ma_don_hang:
                raise ValueError("Mã đơn hàng là bắt buộc")
            return self._model.xoa(ma_don_hang)
        except Exception as e:
            self.handle_error(e, "xóa đơn hàng")
            raise
    
    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)  # Log the error
        return error_message 
    
    def layChiTietDonHang(self, ma_don_hang):
        """Get detailed information for a specific order"""
        try:
            return self._model.layChiTietDonHang(ma_don_hang)
        except Exception as e:
            self.handle_error(e, "lấy chi tiết đơn hàng")
            return None 
    
    def themDonHang(self, data):
        """Add a new order and its details"""
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
        """Get product ID by product name"""
        try:
            return self._model.layMaSanPhamTheoTen(ten_san_pham)
        except Exception as e:
            self.handle_error(e, "lấy mã sản phẩm theo tên")
            return None 