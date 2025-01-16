from app.models.user_model import UserModel
import bcrypt

class UserController:
    def __init__(self):
        self.model = UserModel()

    def layTatCa(self):
        try:
            return self.model.layTatCa()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng: {str(e)}")
            return []

    def layNguoiDungChoDuyet(self):
        try:
            return self.model.layNguoiDungChoDuyet()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng chờ duyệt: {str(e)}")
            return []

    def duyetNguoiDung(self, ma_nguoi_dung):
        try:
            return self.model.duyetNguoiDung(ma_nguoi_dung)
        except Exception as e:
            print(f"Lỗi khi duyệt người dùng: {str(e)}")
            return False

    def tuChoiNguoiDung(self, ma_nguoi_dung):
        try:
            return self.model.tuChoiNguoiDung(ma_nguoi_dung)
        except Exception as e:
            print(f"Lỗi khi từ chối người dùng: {str(e)}")
            return False

    def dangNhap(self, ten_dang_nhap, mat_khau):
        try:
            nguoi_dung = self.model.layTheoTenDangNhap(ten_dang_nhap)
            if not nguoi_dung:
                return False, "Tên đăng nhập hoặc mật khẩu không đúng"
    
            if not bcrypt.checkpw(mat_khau.encode('utf-8'), nguoi_dung['mat_khau'].encode('utf-8')):
                return False, "Tên đăng nhập hoặc mật khẩu không đúng"
    
            user_data = {k: v for k, v in nguoi_dung.items() if k != 'mat_khau'}
            return True, user_data

        except Exception as e:
            return False, f"Lỗi đăng nhập: {str(e)}"

    def dangKy(self, ten_dang_nhap, mat_khau, ho_ten):
        try:
            if self.model.layTheoTenDangNhap(ten_dang_nhap):
                return False, "Tên đăng nhập đã tồn tại"

            if self.model.layTheoHoTen(ho_ten):
                return False, "Họ tên đã tồn tại"

            hashed = bcrypt.hashpw(mat_khau.encode('utf-8'), bcrypt.gensalt())
            
            self.model.taoNguoiDung(ten_dang_nhap, hashed.decode('utf-8'), ho_ten, la_admin=False)
            
            return True, "Đăng ký thành công! Vui lòng chờ quản trị viên duyệt."

        except Exception as e:
            return False, f"Lỗi đăng ký: {str(e)}"

    def layTheoId(self, ma_nguoi_dung):
        try:
            nguoi_dung = self.model.layTheoId(ma_nguoi_dung)
            if nguoi_dung:
                user_data = {k: v for k, v in nguoi_dung.items() if k != 'mat_khau'}
                return True, user_data
            return False, "Không tìm thấy người dùng"
        except Exception as e:
            return False, f"Lỗi khi lấy thông tin người dùng: {str(e)}"

    def capNhatNguoiDung(self, ma_nguoi_dung, data):
        """Update user information"""
        try:
            if 'mat_khau' in data:
                data['mat_khau'] = bcrypt.hashpw(
                    data['mat_khau'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
            
            success = self.model.capNhatNguoiDung(ma_nguoi_dung, data)
            if success:
                return True, "Cập nhật người dùng thành công"
            return False, "Cập nhật người dùng thất bại"
        except Exception as e:
            return False, f"Lỗi khi cập nhật người dùng: {str(e)}"

    def xoaNguoiDung(self, ma_nguoi_dung):
        try:
            success = self.model.xoaNguoiDung(ma_nguoi_dung)
            if success:
                return True, "Xóa người dùng thành công"
            return False, "Không thể xóa người dùng. Vui lòng thử lại sau."
        except Exception as e:
            # Check for foreign key constraint violation (MySQL error 1451)
            if "1451" in str(e):
                return False, "Không thể xóa người dùng này vì họ đã có đơn hàng trong hệ thống. Vui lòng xóa các đơn hàng trước khi xóa người dùng."
            return False, f"Lỗi khi xóa người dùng: {str(e)}"

    def doiMatKhau(self, ma_nguoi_dung, mat_khau_cu, mat_khau_moi):
        try:
            nguoi_dung = self.model.layTheoId(ma_nguoi_dung)
            if not nguoi_dung:
                return False, "Không tìm thấy người dùng"

            if not bcrypt.checkpw(mat_khau_cu.encode('utf-8'), 
                                nguoi_dung['mat_khau'].encode('utf-8')):
                return False, "Mật khẩu hiện tại không đúng"

            hashed = bcrypt.hashpw(mat_khau_moi.encode('utf-8'), bcrypt.gensalt())
            success = self.model.capNhatMatKhau(ma_nguoi_dung, hashed.decode('utf-8'))
            
            if success:
                return True, "Đổi mật khẩu thành công"
            return False, "Đổi mật khẩu thất bại"
            
        except Exception as e:
            return False, f"Lỗi khi đổi mật khẩu: {str(e)}"

    def layVaiTro(self):
        try:
            return self.model.layVaiTro()
        except Exception as e:
            print(f"Lỗi khi lấy vai trò: {str(e)}")
            return []

    def layNguoiDungDaDuyet(self):
        try:
            return self.model.layNguoiDungDaDuyet()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng đã duyệt: {str(e)}")
            return []

    def layNguoiDungPhanTrang(self, offset=0, limit=10, search_query=""):
        try:
            users, total_count = self.model.layNguoiDungPhanTrang(
                offset=offset,
                limit=limit,
                search_query=search_query
            )
            return users, total_count
        except Exception as e:
            print(f"Lỗi khi lấy danh sách người dùng phân trang: {str(e)}")
            return [], 0

    def datVaiTroNguoiDung(self, ma_nguoi_dung, vai_tro_moi):
        try:
            success = self.model.datVaiTroNguoiDung(ma_nguoi_dung, vai_tro_moi)
            if success:
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật vai trò người dùng: {e}")
            return False
