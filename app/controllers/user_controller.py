from app.models.user_model import UserModel
import bcrypt

class UserController:
    def __init__(self):
        self.model = UserModel()

    def layTatCa(self):
        """
        + Input: Không có
        + Output: Danh sách tất cả người dùng trong hệ thống
        + Raises:
            - Exception khi lấy danh sách người dùng thất bại
        """
        try:
            return self.model.layTatCa()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng: {str(e)}")
            return []

    def layNguoiDungChoDuyet(self):
        """
        + Input: Không có
        + Output: Danh sách người dùng đang chờ được duyệt
        + Raises:
            - Exception khi lấy danh sách người dùng chờ duyệt thất bại
        """
        try:
            return self.model.layNguoiDungChoDuyet()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng chờ duyệt: {str(e)}")
            return []

    def duyetNguoiDung(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần duyệt
        + Output: True nếu duyệt thành công, False nếu thất bại
        + Raises:
            - Exception khi duyệt người dùng thất bại
        """
        try:
            return self.model.duyetNguoiDung(ma_nguoi_dung)
        except Exception as e:
            print(f"Lỗi khi duyệt người dùng: {str(e)}")
            return False

    def tuChoiNguoiDung(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần từ chối
        + Output: True nếu từ chối thành công, False nếu thất bại
        + Raises:
            - Exception khi từ chối người dùng thất bại
        """
        try:
            return self.model.tuChoiNguoiDung(ma_nguoi_dung)
        except Exception as e:
            print(f"Lỗi khi từ chối người dùng: {str(e)}")
            return False

    def dangNhap(self, ten_dang_nhap, mat_khau):
        """
        + Input:
            - ten_dang_nhap: Tên đăng nhập
            - mat_khau: Mật khẩu
        + Output: Tuple chứa:
            - Boolean: True nếu đăng nhập thành công, False nếu thất bại
            - Dict/String: Thông tin người dùng nếu thành công, thông báo lỗi nếu thất bại
        + Raises:
            - Exception khi đăng nhập thất bại
        """
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
        """
        + Input:
            - ten_dang_nhap: Tên đăng nhập mới
            - mat_khau: Mật khẩu
            - ho_ten: Họ tên người dùng
        + Output: Tuple chứa:
            - Boolean: True nếu đăng ký thành công, False nếu thất bại
            - String: Thông báo kết quả đăng ký
        + Raises:
            - Exception khi đăng ký thất bại
        """
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
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần tìm
        + Output: Tuple chứa:
            - Boolean: True nếu tìm thấy, False nếu không tìm thấy
            - Dict/String: Thông tin người dùng nếu tìm thấy, thông báo lỗi nếu không tìm thấy
        + Raises:
            - Exception khi lấy thông tin người dùng thất bại
        """
        try:
            nguoi_dung = self.model.layTheoId(ma_nguoi_dung)
            if nguoi_dung:
                user_data = {k: v for k, v in nguoi_dung.items() if k != 'mat_khau'}
                return True, user_data
            return False, "Không tìm thấy người dùng"
        except Exception as e:
            return False, f"Lỗi khi lấy thông tin người dùng: {str(e)}"

    def capNhatNguoiDung(self, ma_nguoi_dung, data):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần cập nhật
            - data: Từ điển chứa thông tin cần cập nhật
        + Output: Tuple chứa:
            - Boolean: True nếu cập nhật thành công, False nếu thất bại
            - String: Thông báo kết quả cập nhật
        + Raises:
            - Exception khi cập nhật thông tin người dùng thất bại
        """
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
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần xóa
        + Output: Tuple chứa:
            - Boolean: True nếu xóa thành công, False nếu thất bại
            - String: Thông báo kết quả xóa
        + Raises:
            - Exception khi xóa người dùng thất bại
        """
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


    def layVaiTro(self):
        """
        + Input: Không có
        + Output: Danh sách các vai trò trong hệ thống
        + Raises:
            - Exception khi lấy danh sách vai trò thất bại
        """
        try:
            return self.model.layVaiTro()
        except Exception as e:
            print(f"Lỗi khi lấy vai trò: {str(e)}")
            return []

    def layNguoiDungDaDuyet(self):
        """
        + Input: Không có
        + Output: Danh sách người dùng đã được duyệt
        + Raises:
            - Exception khi lấy danh sách người dùng đã duyệt thất bại
        """
        try:
            return self.model.layNguoiDungDaDuyet()
        except Exception as e:
            print(f"Lỗi khi lấy người dùng đã duyệt: {str(e)}")
            return []

    def layNguoiDungPhanTrang(self, offset=0, limit=10, search_query=""):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm người dùng (mặc định: "")
        + Output: Tuple chứa:
            - Danh sách người dùng thỏa mãn điều kiện
            - Tổng số người dùng thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi lấy danh sách người dùng thất bại
        """
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
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần đặt vai trò
            - vai_tro_moi: Vai trò mới cần đặt
        + Output: True nếu đặt vai trò thành công, False nếu thất bại
        + Raises:
            - Exception khi cập nhật vai trò người dùng thất bại
        """
        try:
            success = self.model.datVaiTroNguoiDung(ma_nguoi_dung, vai_tro_moi)
            if success:
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật vai trò người dùng: {e}")
            return False
