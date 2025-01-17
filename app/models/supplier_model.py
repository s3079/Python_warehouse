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
    
    def layNhaCungCapPhanTrang(self, offset=0, limit=10, search_query="", name_sort="none", contact_sort="none"):
        """Get paginated suppliers with optional search and sorting"""
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
                query += " ORDER BY ten"  # Default sorting
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Execute query and get results
            suppliers = self._thucThiTruyVan(query, params) or []
            
            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM {self._table_name}"
            if search_query:
                count_query += " WHERE ten LIKE %s OR email LIKE %s OR dien_thoai LIKE %s"
                count_result = self._thucThiTruyVan(count_query, [f"%{search_query}%"] * 3)
            else:
                count_result = self._thucThiTruyVan(count_query)
            
            total_count = count_result[0]['total'] if count_result else 0
            
            return suppliers, total_count
            
        except Exception as e:
            print(f"Lỗi khi lấy nhà cung cấp phân trang: {e}")
            return [], 0
