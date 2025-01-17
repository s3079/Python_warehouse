from app.models.base_model import BaseModel

class InventoryModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "KHOHANG"
    
    def layTatCa(self):
        """Get all inventory items with product names"""
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
        """Add a new inventory item"""
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
        """Update an existing inventory item"""
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
        """Delete an inventory item"""
        query = f"DELETE FROM {self._table_name} WHERE ma_kho = %s"
        cursor = self._thucThiTruyVan(query, (ma_kho,))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def layTheoId(self, ma_kho: int):
        """Get an inventory item by ID with product name"""
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
        """Get paginated inventory items with optional search"""
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