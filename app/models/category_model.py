from app.utils.database import Database
from app.models.base_model import BaseModel

class CategoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "danh_muc"
        self._db = Database()
        self._db.connect()  # Ensure connection is established
    
    # def _thucThiTruyVan(self, query, params=None):
    #     """Execute a query and return results"""
    #     try:
    #         if not self._db._connection or not self._db._connection.is_connected():
    #             self._db.connect()
    #         return self._db.execute_query(query, params)
    #     except Exception as e:
    #         print(f"Database error: {e}")
    #         return None
    
    def layTatCa(self):
        """Get all categories"""
        query = f"""
            SELECT 
                ma_danh_muc, ten, mo_ta, ngay_tao, ngay_cap_nhat
            FROM {self._table_name}
            ORDER BY ten
        """
        return self._thucThiTruyVan(query) or []
        
    def demSanPham(self, ma_danh_muc):
        """Count number of products in a category"""
        query = """
            SELECT COUNT(*) as so_luong
            FROM san_pham 
            WHERE ma_danh_muc = %s
        """
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0]['so_luong'] if result else 0
        
    def them(self, ten: str, mo_ta: str):
        """Add a new category"""
        query = f"INSERT INTO {self._table_name} (ten, mo_ta) VALUES (%s, %s)"
        return self._thucThiTruyVan(query, (ten, mo_ta))
    
    def capNhat(self, ma_danh_muc: int, ten: str, mo_ta: str):
        """Update a category"""
        query = f"UPDATE {self._table_name} SET ten = %s, mo_ta = %s WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ten, mo_ta, ma_danh_muc))
    
    def xoa(self, ma_danh_muc: int):
        """Delete a category"""
        query = f"DELETE FROM {self._table_name} WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ma_danh_muc,))
    
    def layTheoId(self, ma_danh_muc: int):
        """Get a category by id"""
        query = f"SELECT * FROM {self._table_name} WHERE ma_danh_muc = %s"
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0] if result else None
    
    def layTatCaDanhMuc(self):
        """Get all categories"""
        query = f"SELECT ma_danh_muc, ten FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Lỗi trong layTatCaDanhMuc: {str(e)}")
            return []
