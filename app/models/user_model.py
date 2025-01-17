from app.models.base_model import BaseModel

class UserModel(BaseModel):
    def __init__(self):
        """
        + Input: Không có
        + Output: Khởi tạo đối tượng UserModel với tên bảng "NGUOIDUNG"
        """
        super().__init__()
        self._table_name = "NGUOIDUNG"
        self._damBaoTruongDuyet()
        self.current_user_id = None

    def _damBaoTruongDuyet(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects: Đảm bảo cột da_duyet tồn tại trong bảng NGUOIDUNG
        + Raises:
            - Exception khi kiểm tra hoặc thêm cột thất bại
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_NAME = 'NGUOIDUNG'
                AND COLUMN_NAME = 'da_duyet'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE NGUOIDUNG 
                    ADD COLUMN da_duyet BOOLEAN DEFAULT FALSE
                """)
                self.conn.commit()
        except Exception as e:
            print(f"Error ensuring approval column: {str(e)}")

    def layTatCa(self):
        """
        + Input: Không có
        + Output: Danh sách từ điển chứa thông tin người dùng:
            - ma_nguoi_dung: Mã người dùng
            - ten_dang_nhap: Tên đăng nhập
            - ho_ten: Họ tên
            - ma_quyen: Mã quyền
            - ten_quyen: Tên quyền
            - da_duyet: Trạng thái duyệt
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT nd.*, pq.ten_quyen 
            FROM NGUOIDUNG nd
            JOIN PHANQUYEN pq ON nd.ma_quyen = pq.ma_quyen
            ORDER BY nd.ten_dang_nhap
        """)
        return cursor.fetchall()

    def layNguoiDungChoDuyet(self):
        """
        + Input: Không có
        + Output: Danh sách từ điển chứa thông tin người dùng chờ duyệt
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM NGUOIDUNG u
            JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
            WHERE u.da_duyet = FALSE
            ORDER BY u.ten_dang_nhap
        """)
        return cursor.fetchall()

    def duyetNguoiDung(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần duyệt
        + Output: Boolean - True nếu duyệt thành công, False nếu thất bại
        + Raises:
            - Exception khi duyệt người dùng thất bại
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE NGUOIDUNG 
                SET da_duyet = TRUE, ma_quyen = 3
                WHERE ma_nguoi_dung = %s
            """, (ma_nguoi_dung,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi duyệt người dùng: {str(e)}")
            return False

    def tuChoiNguoiDung(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần từ chối
        + Output: Boolean - True nếu từ chối thành công, False nếu thất bại
        + Raises:
            - Exception khi từ chối người dùng thất bại
        """
        return self.xoaNguoiDung(ma_nguoi_dung)

    def taoNguoiDung(self, ten_dang_nhap, mat_khau, ho_ten, la_admin=False):
        """
        + Input:
            - ten_dang_nhap: Tên đăng nhập mới
            - mat_khau: Mật khẩu
            - ho_ten: Họ tên người dùng
            - la_admin: True nếu là admin, False nếu là người dùng thường (mặc định: False)
        + Output: 
            - Mã người dùng mới nếu tạo thành công
            - None nếu tạo thất bại
        + Raises:
            - Exception khi tạo người dùng thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            ten_quyen = 'administrator' if la_admin else 'registered_user'
            cursor.execute(
                "SELECT ma_quyen FROM PHANQUYEN WHERE ten_quyen = %s",
                (ten_quyen,)
            )
            role = cursor.fetchone()
            if not role:
                raise Exception(f"Role '{ten_quyen}' not found")

            cursor.execute("""
                INSERT INTO NGUOIDUNG (ten_dang_nhap, mat_khau, ho_ten, ma_quyen, da_duyet)
                VALUES (%s, %s, %s, %s, %s)
            """, (ten_dang_nhap, mat_khau, ho_ten, role['ma_quyen'], la_admin))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def layTheoTenDangNhap(self, ten_dang_nhap):
        """
        + Input:
            - ten_dang_nhap: Tên đăng nhập cần tìm
        + Output: 
            - Từ điển chứa thông tin người dùng nếu tìm thấy
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM NGUOIDUNG u
            JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
            WHERE u.ten_dang_nhap = %s
        """, (ten_dang_nhap,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def layTheoId(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần tìm
        + Output: 
            - Từ điển chứa thông tin người dùng nếu tìm thấy
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM NGUOIDUNG u
            JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
            WHERE u.ma_nguoi_dung = %s
        """, (ma_nguoi_dung,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def capNhatNguoiDung(self, ma_nguoi_dung, data):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần cập nhật
            - data: Từ điển chứa thông tin cập nhật:
                + ten_dang_nhap: Tên đăng nhập mới
                + ho_ten: Họ tên mới
                + mat_khau: Mật khẩu mới
        + Output: Boolean - True nếu cập nhật thành công, False nếu thất bại
        + Raises:
            - Exception khi cập nhật người dùng thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            update_fields = []
            values = []
            for key, value in data.items():
                if key in ['ten_dang_nhap', 'ho_ten', 'mat_khau']:
                    update_fields.append(f"{key} = %s")
                    values.append(value)

            if not update_fields:
                return False

            values.append(ma_nguoi_dung)

            query = f"""
                UPDATE NGUOIDUNG 
                SET {', '.join(update_fields)}
                WHERE ma_nguoi_dung = %s
            """
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def xoaNguoiDung(self, ma_nguoi_dung):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần xóa
        + Output: Boolean - True nếu xóa thành công, False nếu thất bại
        + Raises:
            - Exception khi xóa người dùng thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                DELETE FROM NGUOIDUNG 
                WHERE ma_nguoi_dung = %s
            """, (ma_nguoi_dung,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def layVaiTro(self):
        """
        + Input: Không có
        + Output: Danh sách các vai trò trong hệ thống (trừ vai trò administrator)
        + Raises:
            - Exception khi truy vấn thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM PHANQUYEN
                WHERE ten_quyen IN ('nguoi_dung', 'quan_ly')
                ORDER BY ten_quyen
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy vai trò: {str(e)}")
            return []

    def layNguoiDungDaDuyet(self):
        """
        + Input: Không có
        + Output: Danh sách người dùng đã được duyệt
        + Raises:
            - Exception khi truy vấn thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.*, r.ten_quyen 
                FROM NGUOIDUNG u
                JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
                WHERE u.da_duyet = TRUE
                ORDER BY u.ten_dang_nhap
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting approved users: {str(e)}")
            return []

    def layNguoiDungPhanTrang(self, offset=0, limit=10, search_query=""):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm (mặc định: "")
        + Output: Tuple chứa:
            - Danh sách từ điển thông tin người dùng thỏa mãn điều kiện
            - Tổng số người dùng thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT u.*, r.ten_quyen 
                FROM NGUOIDUNG u
                JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
            """
            if search_query:
                query += " WHERE u.ten_dang_nhap LIKE %s OR u.ho_ten LIKE %s"
                search_term = f"%{search_query}%"
                cursor.execute(query + " ORDER BY u.ten_dang_nhap LIMIT %s OFFSET %s", 
                             (search_term, search_term, limit, offset))
            else:
                cursor.execute(query + " ORDER BY u.ten_dang_nhap LIMIT %s OFFSET %s", 
                             (limit, offset))
            
            users = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) FROM NGUOIDUNG")
            total_count = cursor.fetchone()['COUNT(*)']

            return users, total_count
        except Exception as e:
            print(f"Lỗi khi lấy danh sách người dùng phân trang: {str(e)}")
            return [], 0
        finally:
            cursor.close()

    def datVaiTroNguoiDung(self, ma_nguoi_dung, ten_quyen):
        """
        + Input:
            - ma_nguoi_dung: Mã người dùng cần đặt vai trò
            - ten_quyen: Tên quyền mới
        + Output: Boolean - True nếu đặt vai trò thành công, False nếu thất bại
        + Raises:
            - Exception khi cập nhật vai trò thất bại
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("SELECT ma_quyen FROM PHANQUYEN WHERE ten_quyen = %s", (ten_quyen,))
            quyen = cursor.fetchone()
            if not quyen:
                print(f"Quyền '{ten_quyen}' không tìm thấy.")
                return False

            cursor.execute("UPDATE NGUOIDUNG SET ma_quyen = %s WHERE ma_nguoi_dung = %s", 
                         (quyen['ma_quyen'], ma_nguoi_dung))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Error in UserModel.datVaiTroNguoiDung: {e}")
            return False
        finally:
            cursor.close()

    def layTheoHoTen(self, ho_ten):
        """
        + Input:
            - ho_ten: Họ tên người dùng cần tìm
        + Output: 
            - Từ điển chứa thông tin người dùng nếu tìm thấy
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM NGUOIDUNG u
            JOIN PHANQUYEN r ON u.ma_quyen = r.ma_quyen
            WHERE u.ho_ten = %s
        """, (ho_ten,))
        result = cursor.fetchone()
        cursor.close()
        return result
