from app.models.base_model import BaseModel

class InventoryModel(BaseModel):
    def __init__(self):
        """
        + Input: Không có
        + Output: Khởi tạo đối tượng InventoryModel với tên bảng "KHOHANG"
        """
        super().__init__()
        self._table_name = "KHOHANG"
    
    def layTatCa(self):
        """
        + Input: Không có
        + Output: Danh sách từ điển chứa thông tin kho hàng:
            - ma_kho: Mã kho hàng
            - ten_san_pham: Tên sản phẩm
            - so_luong: Số lượng tồn kho
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"""
            SELECT 
                i.ma_kho,
                p.ten as ten_san_pham,
                i.so_luong
            FROM {self._table_name} i
            LEFT JOIN san_pham p ON i.ma_san_pham = p.ma_san_pham
            ORDER BY p.ten
        """
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def them(self, **data):
        """
        + Input:
            - data: Từ điển chứa thông tin kho hàng mới:
                + ma_san_pham: Mã sản phẩm
                + so_luong: Số lượng
                + ngay_nhap_cuoi: Ngày nhập kho cuối cùng
        + Output: Tuple chứa:
            - Boolean: True nếu thêm thành công, False nếu thất bại
            - String: Thông báo kết quả
        + Raises:
            - Exception khi thêm kho hàng thất bại
        """
        query = f"""
            INSERT INTO {self._table_name} 
            (ma_san_pham, so_luong, ngay_nhap_cuoi)
            VALUES (%s, %s, %s)
        """
        params = (
            data.get('ma_san_pham'),
            data.get('so_luong'),
            data.get('ngay_nhap_cuoi')
        )
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True, "Thêm kho hàng thành công"
        return False, "Thêm kho hàng thất bại"
    
    def capNhat(self, data):
        """
        + Input:
            - data: Từ điển chứa thông tin cập nhật:
                + ma_kho: Mã kho hàng cần cập nhật
                + ma_san_pham: Mã sản phẩm mới
                + so_luong: Số lượng mới
                + ngay_nhap_cuoi: Ngày nhập kho cuối cùng mới
        + Output: Boolean - True nếu cập nhật thành công, False nếu thất bại
        + Raises:
            - Exception khi cập nhật kho hàng thất bại
        """
        query = f"""
            UPDATE {self._table_name}
            SET ma_san_pham = %s, 
                so_luong = %s,
                ngay_nhap_cuoi = %s
            WHERE ma_kho = %s
        """
        cursor = self._thucThiTruyVan(query, (
            data.get('ma_san_pham'),
            data.get('so_luong'),
            data.get('ngay_nhap_cuoi'),
            data.get('ma_kho')
        ))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def xoa(self, ma_kho: int):
        """
        + Input:
            - ma_kho: Mã kho hàng cần xóa
        + Output: Boolean - True nếu xóa thành công, False nếu thất bại
        + Raises:
            - Exception khi xóa kho hàng thất bại
        """
        query = f"DELETE FROM {self._table_name} WHERE ma_kho = %s"
        cursor = self._thucThiTruyVan(query, (ma_kho,))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def layTheoId(self, ma_kho: int):
        """
        + Input:
            - ma_kho: Mã kho hàng cần tìm
        + Output: 
            - Từ điển chứa thông tin kho hàng nếu tìm thấy:
                + ma_kho: Mã kho hàng
                + so_luong: Số lượng tồn kho
                + ten_san_pham: Tên sản phẩm
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"""
            SELECT 
                i.ma_kho, i.so_luong,
                p.ten as ten_san_pham
            FROM {self._table_name} i
            LEFT JOIN san_pham p ON i.ma_san_pham = p.ma_san_pham
            WHERE i.ma_kho = %s
        """
        cursor = self._thucThiTruyVan(query, (ma_kho,))
        return cursor.fetchone() if cursor else None
    
    def layKhoHangPhanTrang(self, offset=0, limit=10, search_query=""):
        """
        + Input:
            - offset: Số bản ghi bỏ qua (mặc định: 0)
            - limit: Số lượng bản ghi tối đa trả về (mặc định: 10)
            - search_query: Từ khóa tìm kiếm theo tên sản phẩm (mặc định: "")
        + Output: Tuple chứa:
            - Danh sách từ điển thông tin kho hàng thỏa mãn điều kiện
            - Tổng số kho hàng thỏa mãn điều kiện tìm kiếm
        + Raises:
            - Exception khi truy vấn thất bại
        """
        try:
            query = """
                SELECT i.*, p.ten as ten_san_pham
                FROM KHOHANG i
                LEFT JOIN SANPHAM p ON i.ma_san_pham = p.ma_san_pham
            """
            count_query = "SELECT COUNT(*) FROM KHOHANG i"
            
            params = []
            
            if search_query:
                query += " WHERE p.ten LIKE %s"
                count_query += " LEFT JOIN SANPHAM p ON i.ma_san_pham = p.ma_san_pham WHERE p.ten LIKE %s"
                params.append(f"%{search_query}%")
            
            query += " ORDER BY i.ngay_nhap_cuoi DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor = self.conn.cursor()
            if search_query:
                cursor.execute(count_query, [f"%{search_query}%"])
            else:
                cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            cursor.execute(query, params)
            inventory = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            inventory = [dict(zip(columns, item)) for item in inventory]
            
            return inventory, total_count
            
        except Exception as e:
            print(f"Lỗi khi lấy danh sách kho hàng phân trang: {e}")
            return [], 0