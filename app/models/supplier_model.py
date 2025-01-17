from app.models.base_model import BaseModel

class SupplierModel(BaseModel):
    def __init__(self):
        """
        + Input: Không có
        + Output: Khởi tạo đối tượng SupplierModel với tên bảng "NHACUNGCAP"
        """
        super().__init__()
        self._table_name = "NHACUNGCAP"
    
    def layTatCa(self):
        """
        + Input: Không có
        + Output: Danh sách từ điển chứa thông tin nhà cung cấp:
            - ma_ncc: Mã nhà cung cấp
            - ten: Tên nhà cung cấp
            - dia_chi: Địa chỉ
            - dien_thoai: Số điện thoại
            - email: Email
            - ngay_tao: Ngày tạo
            - ngay_cap_nhat: Ngày cập nhật
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"SELECT * FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Error in layTatCa: {str(e)}")
            return []
    
    def them(self, **data):
        """
        + Input:
            - data: Từ điển chứa thông tin nhà cung cấp mới:
                + ten: Tên nhà cung cấp
                + dia_chi: Địa chỉ
                + dien_thoai: Số điện thoại
                + email: Email
        + Output: Tuple chứa:
            - Boolean: True nếu thêm thành công, False nếu thất bại
            - String: Thông báo kết quả
        + Raises:
            - Exception khi thêm nhà cung cấp thất bại
        """
        query = f"""
            INSERT INTO {self._table_name} 
            (ten, dia_chi, dien_thoai, email) 
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data.get('ten'),
            data.get('dia_chi'),
            data.get('dien_thoai'),
            data.get('email')
        )
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True, "Supplier added successfully"
        return False, "Failed to add supplier"
    
    def capNhat(self, data):
        """
        + Input:
            - data: Từ điển chứa thông tin cập nhật:
                + ma_ncc: Mã nhà cung cấp cần cập nhật
                + ten: Tên nhà cung cấp mới
                + dia_chi: Địa chỉ mới
                + dien_thoai: Số điện thoại mới
                + email: Email mới
        + Output: Boolean - True nếu cập nhật thành công, False nếu thất bại
        + Raises:
            - Exception khi cập nhật nhà cung cấp thất bại
        """
        query = f"""
            UPDATE {self._table_name}
            SET ten = %s, dia_chi = %s, dien_thoai = %s, email = %s
            WHERE ma_ncc = %s
        """
        params = (
            data.get('ten'),
            data.get('dia_chi'),
            data.get('dien_thoai'),
            data.get('email'),
            data.get('ma_ncc')
        )
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def xoa(self, ma_ncc: int):
        """
        + Input:
            - ma_ncc: Mã nhà cung cấp cần xóa
        + Output: Boolean - True nếu xóa thành công, False nếu thất bại
        + Raises:
            - Exception khi xóa nhà cung cấp thất bại
        """
        query = f"DELETE FROM {self._table_name} WHERE ma_ncc = %s"
        cursor = self._thucThiTruyVan(query, (ma_ncc,))
        if cursor:
            self.conn.commit()
            return True
        return False

    def layTheoId(self, ma_ncc: int):
        """
        + Input:
            - ma_ncc: Mã nhà cung cấp cần tìm
        + Output: 
            - Từ điển chứa thông tin nhà cung cấp nếu tìm thấy
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"SELECT * FROM {self._table_name} WHERE ma_ncc = %s"
        result = self._thucThiTruyVan(query, (ma_ncc,))
        return result[0] if result else None
    
    def layNhaCungCapPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", contact_sort="none"):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm (mặc định: "")
            - name_sort: Hướng sắp xếp theo tên ('asc', 'desc', 'none') (mặc định: "none")
            - contact_sort: Hướng sắp xếp theo số điện thoại ('asc', 'desc', 'none') (mặc định: "none")
        + Output: Tuple chứa:
            - Danh sách từ điển thông tin nhà cung cấp thỏa mãn điều kiện
            - Tổng số nhà cung cấp thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi truy vấn thất bại
        """
        try:
            query = f"""
                SELECT 
                    ma_ncc, ten, email, dien_thoai, dia_chi, 
                    ngay_tao, ngay_cap_nhat
                FROM {self._table_name}
                WHERE 1=1
            """
            params = []
            
            # Add search conditions if search_query exists
            if search_query:
                query += " AND (ten LIKE %s OR email LIKE %s OR dien_thoai LIKE %s)"
                params.extend([f"%{search_query}%"] * 3)
            
            # Add ORDER BY clause based on sorting preferences
            order_clauses = []
            if name_sort in ["asc", "desc"]:
                order_clauses.append(f"ten {name_sort}")
            if contact_sort in ["asc", "desc"]:
                order_clauses.append(f"dien_thoai {contact_sort}")
            
            if order_clauses:
                query += " ORDER BY " + ", ".join(order_clauses)
            else:
                query += " ORDER BY ten" 
            
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            suppliers = self._thucThiTruyVan(query, params) or []
            
            count_query = f"SELECT COUNT(*) as total FROM {self._table_name}"
            if search_query:
                count_query += " WHERE ten LIKE %s OR email LIKE %s OR dien_thoai LIKE %s"
                count_result = self._thucThiTruyVan(count_query, [f"%{search_query}%"] * 3)
            else:
                count_result = self._thucThiTruyVan(count_query)
            
            total_count = count_result[0]['total'] if count_result else 0
            
            return suppliers, total_count
            
        except Exception as e:
            return [], 0
