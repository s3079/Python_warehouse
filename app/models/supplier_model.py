from app.models.base_model import BaseModel

class SupplierModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "NHACUNGCAP"
    
    def layTatCa(self):
        """Get all suppliers"""
        query = f"SELECT * FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Error in layTatCa: {str(e)}")
            return []
    
    def them(self, **data):
        """Add a new supplier"""
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
    
    def capNhat(self,data):
        """Update an existing supplier"""
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
        """Delete a supplier"""
        query = f"DELETE FROM {self._table_name} WHERE ma_ncc = %s"
        cursor = self._thucThiTruyVan(query, (ma_ncc,))
        if cursor:
            self.conn.commit()
            return True
        return False

    def layTheoId(self, ma_ncc: int):
        """Get a supplier by id"""
        query = f"SELECT * FROM {self._table_name} WHERE ma_ncc = %s"
        result = self._thucThiTruyVan(query, (ma_ncc,))
        return result[0] if result else None
    
    def layNhaCungCapPhanTrang(self, offset=0, limit=10, search_query=""):
        """Get paginated suppliers with optional search"""
        try:
            query = f"SELECT * FROM {self._table_name}"
            count_query = f"SELECT COUNT(*) FROM {self._table_name}"
            
            params = []
            
            if search_query:
                query += " WHERE ten LIKE %s OR email LIKE %s"
                count_query += " WHERE ten LIKE %s OR email LIKE %s"
                params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
            
            query += " ORDER BY ten LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor = self.conn.cursor()
            if search_query:
                cursor.execute(count_query, params[:3])
            else:
                cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            cursor.execute(query, params)
            suppliers = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            suppliers = [dict(zip(columns, supplier)) for supplier in suppliers]
            
            return suppliers, total_count
            
        except Exception as e:
            print(f"Lỗi khi lấy nhà cung cấp phân trang: {e}")
            return [], 0
