from app.models.base_model import BaseModel

class CategoryModel(BaseModel):
    def __init__(self):
        """
        + Input: Không có
        + Output: Khởi tạo đối tượng CategoryModel với tên bảng "DANHMUC"
        """
        super().__init__()
        self._table_name = "DANHMUC"

    def layTatCa(self, name_sort="none", desc_sort="none"):
        """
        + Input:
            - name_sort: Hướng sắp xếp theo tên ('asc', 'desc', 'none') (mặc định: "none")
            - desc_sort: Hướng sắp xếp theo mô tả ('asc', 'desc', 'none') (mặc định: "none")
        + Output: Danh sách từ điển chứa thông tin danh mục:
            - ma_danh_muc: Mã danh mục
            - ten: Tên danh mục
            - mo_ta: Mô tả danh mục
            - ngay_tao: Ngày tạo
            - ngay_cap_nhat: Ngày cập nhật
        """
        query = f"""
            SELECT 
                ma_danh_muc, ten, mo_ta, ngay_tao, ngay_cap_nhat
            FROM {self._table_name}
            WHERE 1=1
        """
        
        order_clauses = []
        if name_sort in ["asc", "desc"]:
            order_clauses.append(f"ten {name_sort}")
        if desc_sort in ["asc", "desc"]:
            order_clauses.append(f"mo_ta {desc_sort}")
        
        if order_clauses:
            query += " ORDER BY " + ", ".join(order_clauses)
        
        return self._thucThiTruyVan(query) or []
        
    def demSanPham(self, ma_danh_muc):
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần đếm số sản phẩm
        + Output: Số lượng sản phẩm trong danh mục
        """
        query = """
            SELECT COUNT(*) as so_luong
            FROM SANPHAM 
            WHERE ma_danh_muc = %s
        """
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0]['so_luong'] if result else 0
        
    def them(self, ten: str, mo_ta: str):
        """
        + Input:
            - ten: Tên danh mục mới
            - mo_ta: Mô tả danh mục mới
        + Output: Kết quả thực thi truy vấn thêm danh mục
        + Raises:
            - Exception khi thêm danh mục thất bại
        """
        query = f"INSERT INTO {self._table_name} (ten, mo_ta) VALUES (%s, %s)"
        return self._thucThiTruyVan(query, (ten, mo_ta))
    
    def capNhat(self, ma_danh_muc: int, ten: str, mo_ta: str):
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần cập nhật
            - ten: Tên danh mục mới
            - mo_ta: Mô tả danh mục mới
        + Output: Kết quả thực thi truy vấn cập nhật danh mục
        + Raises:
            - Exception khi cập nhật danh mục thất bại
        """
        query = f"UPDATE {self._table_name} SET ten = %s, mo_ta = %s WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ten, mo_ta, ma_danh_muc))
    
    def xoa(self, ma_danh_muc: int):
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần xóa
        + Output: Kết quả thực thi truy vấn xóa danh mục
        + Raises:
            - Exception khi xóa danh mục thất bại
        """
        query = f"DELETE FROM {self._table_name} WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ma_danh_muc,))
    
    def layTheoId(self, ma_danh_muc: int):
        """
        + Input:
            - ma_danh_muc: Mã danh mục cần tìm
        + Output: 
            - Từ điển chứa thông tin danh mục nếu tìm thấy
            - None nếu không tìm thấy
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"SELECT * FROM {self._table_name} WHERE ma_danh_muc = %s"
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0] if result else None
    
    def layTatCaDanhMuc(self):
        """
        + Input: Không có
        + Output: Danh sách từ điển chứa thông tin cơ bản của danh mục:
            - ma_danh_muc: Mã danh mục
            - ten: Tên danh mục
        + Raises:
            - Exception khi truy vấn thất bại
        """
        query = f"SELECT ma_danh_muc, ten FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Lỗi trong layTatCaDanhMuc: {str(e)}")
            return []
