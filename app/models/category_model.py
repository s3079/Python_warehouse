from app.utils.database import Database
from app.models.base_model import BaseModel

class CategoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "DANHMUC"

    def layTatCa(self, name_sort="none", desc_sort="none"):
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
        query = """
            SELECT COUNT(*) as so_luong
            FROM SANPHAM 
            WHERE ma_danh_muc = %s
        """
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0]['so_luong'] if result else 0
        
    def them(self, ten: str, mo_ta: str):
        query = f"INSERT INTO {self._table_name} (ten, mo_ta) VALUES (%s, %s)"
        return self._thucThiTruyVan(query, (ten, mo_ta))
    
    def capNhat(self, ma_danh_muc: int, ten: str, mo_ta: str):
        query = f"UPDATE {self._table_name} SET ten = %s, mo_ta = %s WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ten, mo_ta, ma_danh_muc))
    
    def xoa(self, ma_danh_muc: int):
        query = f"DELETE FROM {self._table_name} WHERE ma_danh_muc = %s"
        return self._thucThiTruyVan(query, (ma_danh_muc,))
    
    def layTheoId(self, ma_danh_muc: int):
        query = f"SELECT * FROM {self._table_name} WHERE ma_danh_muc = %s"
        result = self._thucThiTruyVan(query, (ma_danh_muc,))
        return result[0] if result else None
    
    def layTatCaDanhMuc(self):
        query = f"SELECT ma_danh_muc, ten FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Lỗi trong layTatCaDanhMuc: {str(e)}")
            return []
