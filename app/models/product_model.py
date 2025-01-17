from app.models.base_model import BaseModel

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "SANPHAM"
    
    def layTatCa(self):
        query = f"""
            SELECT 
                sp.ma_san_pham,
                sp.ten,
                sp.mo_ta,
                sp.don_gia,
                sp.ma_danh_muc,
                sp.ma_ncc,
                sp.ngay_tao,
                sp.ngay_cap_nhat,
                dm.ten as ten_danh_muc,
                ncc.ten as ten_nha_cung_cap
            FROM {self._table_name} sp
            LEFT JOIN DANHMUC dm ON sp.ma_danh_muc = dm.ma_danh_muc
            LEFT JOIN NHACUNGCAP ncc ON sp.ma_ncc = ncc.ma_ncc
            ORDER BY sp.ten
        """
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Error in get_all: {str(e)}")
            return []
    
    def them(self, **data):
        query = f"""
            INSERT INTO {self._table_name} 
            (ten, mo_ta, don_gia, ma_danh_muc, ma_ncc)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data.get('ten'),
            data.get('mo_ta'),
            data.get('don_gia'),
            data.get('ma_danh_muc'),
            data.get('ma_ncc')
        )
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True, "Thêm sản phẩm thành công"
        return False, "Thêm sản phẩm thất bại"
    
    def layTatCaVoiTen(self):
        query = f"""
            SELECT 
                p.ma_san_pham,
                p.ten,
                p.mo_ta,
                p.don_gia,
                p.ma_danh_muc,
                p.ma_ncc,
                c.ten as ten_danh_muc,
                s.ten as ten_ncc
            FROM {self._table_name} p
            LEFT JOIN DANHMUC c ON p.ma_danh_muc = c.ma_danh_muc
            LEFT JOIN NHACUNGCAP s ON p.ma_ncc = s.ma_ncc
            ORDER BY p.ten
        """
        cursor = self._thucThiTruyVan(query)
        return cursor.fetchall() if cursor else []
    
    def capNhat(self, ma_san_pham: int, ten: str, mo_ta: str, 
               don_gia: float, ma_danh_muc: int = None, ma_ncc: int = None):
        query = f"""
            UPDATE {self._table_name}
            SET ten = %s, mo_ta = %s, don_gia = %s, 
                ma_danh_muc = %s, ma_ncc = %s
            WHERE ma_san_pham = %s
        """
        cursor = self._thucThiTruyVan(query, (ten, mo_ta, don_gia,
                                         ma_danh_muc, ma_ncc, ma_san_pham))
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def xoa(self, ma_san_pham: int):
        query = f"DELETE FROM {self._table_name} WHERE ma_san_pham = %s"
        try:
            cursor = self._thucThiTruyVan(query, (ma_san_pham,))
            if cursor:
                self.conn.commit()
                return True, "Xóa sản phẩm thành công"
        except Exception as e:
            if "foreign key constraint fails" in str(e):
                return False, "Không thể xóa sản phẩm này vì nó đang được sử dụng trong đơn hàng"
            return False, f"Lỗi khi xóa sản phẩm: {str(e)}"
        return False, "Xóa sản phẩm thất bại"
    
    def layTheoId(self, ma_san_pham: int):
        query = f"""
            SELECT 
                p.ma_san_pham, p.ten, p.mo_ta, p.don_gia,
                p.ma_danh_muc, p.ma_ncc, p.ngay_tao, p.ngay_cap_nhat,
                c.ten as ten_danh_muc, s.ten as ten_ncc
            FROM {self._table_name} p
            LEFT JOIN DANHMUC c ON p.ma_danh_muc = c.ma_danh_muc
            LEFT JOIN NHACUNGCAP s ON p.ma_ncc = s.ma_ncc
            WHERE p.ma_san_pham = %s
        """
        cursor = self._thucThiTruyVan(query, (ma_san_pham,))
        return cursor.fetchone() if cursor else None
    
    def laySanPhamPhanTrang(self, offset=0, limit=10, search_query="", filters=None):
        try:
            query = """
                SELECT p.*, c.ten as ten_danh_muc, s.ten as ten_ncc
                FROM SANPHAM p
                LEFT JOIN DANHMUC c ON p.ma_danh_muc = c.ma_danh_muc
                LEFT JOIN NHACUNGCAP s ON p.ma_ncc = s.ma_ncc
            """
            count_query = "SELECT COUNT(*) FROM SANPHAM p"
            
            where_conditions = []
            params = []
            
            if search_query:
                where_conditions.append("(p.ten LIKE %s OR p.mo_ta LIKE %s)")
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            
            if filters:
                if filters.get('ma_danh_muc'):
                    where_conditions.append("p.ma_danh_muc = %s")
                    params.append(filters['ma_danh_muc'])
                if filters.get('ma_ncc'):
                    where_conditions.append("p.ma_ncc = %s")
                    params.append(filters['ma_ncc'])
                if filters.get('don_gia_min'):
                    where_conditions.append("p.don_gia >= %s")
                    params.append(filters['don_gia_min'])
                if filters.get('don_gia_max'):
                    where_conditions.append("p.don_gia <= %s")
                    params.append(filters['don_gia_max'])
            
            if where_conditions:
                where_clause = " WHERE " + " AND ".join(where_conditions)
                query += where_clause
                count_query += where_clause

            order_by_clauses = []
            if filters and filters.get('name_sort') in ['ASC', 'DESC']:
                order_by_clauses.append(f"p.ten {filters['name_sort']}")
            if filters and filters.get('price_sort') in ['ASC', 'DESC']:
                order_by_clauses.append(f"p.don_gia {filters['price_sort']}")
            
            if order_by_clauses:
                query += " ORDER BY " + ", ".join(order_by_clauses)
            else:
                query += " ORDER BY p.ten"
            
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor = self.conn.cursor()
            cursor.execute(count_query, params[:-2] if params else None)
            total_count = cursor.fetchone()[0]
            
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            products = [dict(zip(columns, product)) for product in products]
            
            return products, total_count
            
        except Exception as e:
            print(f"Lỗi khi lấy sản phẩm phân trang: {e}")
            return [], 0
    
    def layTatCaSanPham(self):
        query = f"SELECT ma_san_pham, ten FROM {self._table_name} ORDER BY ten"
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Lỗi trong layTatCaSanPham: {str(e)}")
            return []
    
    def layTheoTen(self, ten_san_pham):
        query = f"SELECT ma_san_pham, ten FROM {self._table_name} WHERE ten = %s"
        try:
            cursor = self._thucThiTruyVan(query, (ten_san_pham,))
            return cursor.fetchone() if cursor else None
        except Exception as e:
            print(f"Lỗi trong layTheoTen: {str(e)}")
            return None