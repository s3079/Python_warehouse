from app.models.base_model import BaseModel

class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "nguoi_dung"
        self._damBaoTruongDuyet()
        self.current_user_id = None

    def _damBaoTruongDuyet(self):
        """Ensure the approval_status column exists"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_NAME = 'nguoi_dung' 
                AND COLUMN_NAME = 'da_duyet'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE nguoi_dung 
                    ADD COLUMN da_duyet BOOLEAN DEFAULT FALSE
                """)
                self.conn.commit()
        except Exception as e:
            print(f"Error ensuring approval column: {str(e)}")

    def layTatCa(self):
        """Get all users with their roles and approval status"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT nd.*, pq.ten_quyen 
            FROM nguoi_dung nd
            JOIN phan_quyen pq ON nd.ma_quyen = pq.ma_quyen
            ORDER BY nd.ten_dang_nhap
        """)
        return cursor.fetchall()

    def layNguoiDungChoDuyet(self):
        """Get users pending approval"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM nguoi_dung u
            JOIN phan_quyen r ON u.ma_quyen = r.ma_quyen
            WHERE u.da_duyet = FALSE
            ORDER BY u.ten_dang_nhap
        """)
        return cursor.fetchall()

    def duyetNguoiDung(self, ma_nguoi_dung):
        """Approve a user and set role to normal user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE nguoi_dung 
                SET da_duyet = TRUE, ma_quyen = 3
                WHERE ma_nguoi_dung = %s
            """, (ma_nguoi_dung,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi duyệt người dùng: {str(e)}")
            return False

    def tuChoiNguoiDung(self, ma_nguoi_dung):
        """Reject and delete a user"""
        return self.xoaNguoiDung(ma_nguoi_dung)

    def taoNguoiDung(self, ten_dang_nhap, mat_khau, ho_ten, la_admin=False):
        """Create a new user"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            # Get role ID
            ten_quyen = 'quan_tri_vien' if la_admin else 'nguoi_dung_moi'
            cursor.execute(
                "SELECT ma_quyen FROM phan_quyen WHERE ten_quyen = %s",
                (ten_quyen,)
            )
            role = cursor.fetchone()
            if not role:
                raise Exception(f"Role '{ten_quyen}' not found")

            cursor.execute("""
                INSERT INTO users (username, password, fullName, role_id, is_approved)
                VALUES (%s, %s, %s, %s, %s)
            """, (ten_dang_nhap, mat_khau, ho_ten, role['role_id'], la_admin))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def xacThucDangNhap(self, ten_dang_nhap, mat_khau):
        """Verify login credentials and approval status"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM nguoi_dung u
            JOIN phan_quyen r ON u.ma_quyen = r.ma_quyen
            WHERE u.ten_dang_nhap = %s AND u.mat_khau = %s
        """, (ten_dang_nhap, mat_khau))
        user = cursor.fetchone()
        
        if not user:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng"
        
        if not user['da_duyet'] and user['ten_quyen'] != 'quan_tri_vien':
            return False, "Tài khoản của bạn đang chờ duyệt"
            
        return True, user

    def them(self, data):
        """Add a new user - implemented through taoNguoiDung method"""
        return self.taoNguoiDung(
            username=data['username'],
            password=data['password'],
            fullName=data['fullName'],
            is_admin=data.get('is_admin', False)
        )

    def capNhat(self, id, data):
        """Update a user - implemented through capNhatNguoiDung method"""
        return self.capNhatNguoiDung(id, data)

    def xoa(self, id):
        """Delete a user - implemented through xoaNguoiDung method"""
        return self.xoaNguoiDung(id)

    def layTheoTenDangNhap(self, ten_dang_nhap):
        """Get user by username"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM nguoi_dung u
            JOIN phan_quyen r ON u.ma_quyen = r.ma_quyen
            WHERE u.ten_dang_nhap = %s
        """, (ten_dang_nhap,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def layTheoEmail(self, email):
        """Get user by email"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.email = %s
        """, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def layTheoId(self, ma_nguoi_dung):
        """Get user by ID"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.ten_quyen 
            FROM nguoi_dung u
            JOIN phan_quyen r ON u.ma_quyen = r.ma_quyen
            WHERE u.ma_nguoi_dung = %s
        """, (ma_nguoi_dung,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def capNhatNguoiDung(self, ma_nguoi_dung, data):
        """Update user information"""
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
                UPDATE nguoi_dung 
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

    def capNhatMatKhau(self, ma_nguoi_dung, mat_khau_moi):
        """Update user password"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE nguoi_dung 
                SET mat_khau = %s
                WHERE ma_nguoi_dung = %s
            """, (mat_khau_moi, ma_nguoi_dung))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def xoaNguoiDung(self, ma_nguoi_dung):
        """Delete a user"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                DELETE FROM nguoi_dung 
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
        """Get all user roles except administrator"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM phan_quyen
                WHERE ten_quyen IN ('nguoi_dung', 'quan_ly')
                ORDER BY ten_quyen
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi lấy vai trò: {str(e)}")
            return []

    def layNguoiDungDaDuyet(self):
        """Get approved users"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.*, r.role_name 
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
                WHERE u.is_approved = TRUE
                ORDER BY u.username
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting approved users: {str(e)}")
            return []

    def layNguoiDungPhanTrang(self, offset=0, limit=10, search_query=""):
        """Get users with pagination and optional search query"""
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT u.*, r.ten_quyen 
                FROM nguoi_dung u
                JOIN phan_quyen r ON u.ma_quyen = r.ma_quyen
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

            cursor.execute("SELECT COUNT(*) FROM nguoi_dung")
            total_count = cursor.fetchone()['COUNT(*)']

            return users, total_count
        except Exception as e:
            print(f"Lỗi khi lấy danh sách người dùng phân trang: {str(e)}")
            return [], 0
        finally:
            cursor.close()

    def datVaiTroNguoiDung(self, user_id, new_role):
        """Update the role of a user identified by user_id."""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("SELECT role_id FROM user_roles WHERE role_name = %s", (new_role,))
            role = cursor.fetchone()
            if not role:
                print(f"Role '{new_role}' not found.")
                return False

            cursor.execute("UPDATE users SET role_id = %s WHERE user_id = %s", 
                         (role['role_id'], user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Error in UserModel.datVaiTroNguoiDung: {e}")
            return False
        finally:
            cursor.close()

    def layTheoHoTen(self, fullName):
        """Get user by full name"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.fullName = %s
        """, (fullName,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def layIdNguoiDungHienTai(self):
        """Get the ID of the currently logged-in user"""
        return self.current_user_id
    
    def datIdNguoiDungHienTai(self, user_id):
        """Set the current user ID after successful login"""
        self.current_user_id = user_id
