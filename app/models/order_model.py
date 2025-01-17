from app.models.base_model import BaseModel

class OrderModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._table_name = "DONHANG"
    
    def layTatCa(self):
        """Get all orders"""
        query = f"""
            SELECT 
                dh.ma_don_hang,
                dh.ngay_dat,
                dh.tong_tien,
                dh.ngay_tao,
                dh.ngay_cap_nhat
            FROM {self._table_name} dh
            ORDER BY dh.ngay_dat DESC
        """
        try:
            return self._thucThiTruyVan(query) or []
        except Exception as e:
            print(f"Error in layTatCa: {str(e)}")
            return []
    
    def layDonHangPhanTrang(self, offset=0, limit=10):
        """Get paginated orders with optional search"""
        try:
            # Base query
            query = f"""
                SELECT o.*
                FROM {self._table_name} o
            """
            count_query = f"SELECT COUNT(*) FROM {self._table_name} o"
            
            params = []
            
            # Add pagination
            query += " ORDER BY o.ngay_dat DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Get total count
            cursor = self.conn.cursor()
            cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
            
            # Get paginated results
            cursor.execute(query, params)
            orders = cursor.fetchall()
            
            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            orders = [dict(zip(columns, order)) for order in orders]
            
            return orders, total_count
            
        except Exception as e:
            print(f"Error getting paginated orders: {e}")
            return [], 0
    
    def capNhat(self, order_id: int, data: dict):
        """Update an existing order"""
        query = f"""
            UPDATE {self._table_name}
            SET order_date = %s, total_amount = %s
            WHERE order_id = %s
        """
        params = (
            data.get('order_date'),
            data.get('total_amount'),
            order_id
        )
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False
    
    def xoa(self, ma_don_hang: int):
        """Delete an order and its details"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # First delete from chi_tiet_don_hang (child table)
            details_query = "DELETE FROM CHITIETDONHANG WHERE ma_don_hang = %s"
            cursor.execute(details_query, (ma_don_hang,))
            
            # Then delete from don_hang (parent table)
            order_query = f"DELETE FROM {self._table_name} WHERE ma_don_hang = %s"
            cursor.execute(order_query, (ma_don_hang,))
            
            # Commit the transaction
            self.conn.commit()
            return True
            
        except Exception as e:
            # Rollback in case of error
            self.conn.rollback()
            print(f"Error deleting order: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def them(self, ngay_dat, tong_tien, ma_nguoi_dung):
        """Add a new order"""
        query = f"""
            INSERT INTO {self._table_name} 
            (ngay_dat, tong_tien, ma_nguoi_dung)
            VALUES (%s, %s, %s)
        """
        params = (ngay_dat, tong_tien, ma_nguoi_dung)
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False 
    
    def layChiTietDonHang(self, ma_don_hang):
        """Get detailed information for a specific order"""
        try:
            # Get order header information
            header_query = f"""
                SELECT 
                    dh.ma_don_hang,
                    dh.ngay_dat,
                    dh.tong_tien,
                    nd.ten_dang_nhap as ten_nguoi_mua
                FROM {self._table_name} dh
                JOIN NGUOIDUNG nd ON dh.ma_nguoi_dung = nd.ma_nguoi_dung
                WHERE dh.ma_don_hang = %s
            """
            
            # Get order details
            details_query = """
                SELECT 
                    ctdh.so_luong,
                    ctdh.don_gia,
                    sp.ten as ten_san_pham,
                    sp.ma_san_pham
                FROM CHITIETDONHANG ctdh
                JOIN SANPHAM sp ON ctdh.ma_san_pham = sp.ma_san_pham
                WHERE ctdh.ma_don_hang = %s
            """
            
            # Execute header query
            header_result = self._thucThiTruyVan(header_query, (ma_don_hang,))
            if not header_result:
                return None
            
            header = header_result[0]
            order_info = {
                "ma_don_hang": header["ma_don_hang"],
                "ngay_dat": header["ngay_dat"],
                "tong_tien": header["tong_tien"],
                "ten_nguoi_mua": header["ten_nguoi_mua"],
                "ma_san_pham": "",
                "ten_san_pham": "",
                "so_luong": "",
                "don_gia": ""
            }

            details_result = self._thucThiTruyVan(details_query, (ma_don_hang,))
            if details_result:
                order_info["ma_san_pham"] = details_result[0]["ma_san_pham"]
                order_info["ten_san_pham"] = details_result[0]["ten_san_pham"]
                order_info["so_luong"] = details_result[0]["so_luong"]
                order_info["don_gia"] = details_result[0]["don_gia"]
            
            return order_info
            
        except Exception as e:
            print(f"Error getting order details: {e}")
            return None
    
    def themChiTietDonHang(self, ma_don_hang, ma_san_pham, so_luong, don_gia):
        """Add a new order detail"""
        query = f"""
            INSERT INTO CHITIETDONHANG 
            (ma_don_hang, ma_san_pham, so_luong, don_gia)
            VALUES (%s, %s, %s, %s)
        """
        params = (ma_don_hang, ma_san_pham, so_luong, don_gia)
        cursor = self._thucThiTruyVan(query, params)
        if cursor:
            self.conn.commit()
            return True
        return False 
    
    def capNhatDonHang(self, ma_don_hang, ngay_dat, so_luong, tong_tien, ma_san_pham, ma_nguoi_dung, don_gia):
        """Update an existing order and its details"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # Update main order
            order_query = f"""
                UPDATE {self._table_name}
                SET ngay_dat = %s,
                    tong_tien = %s,
                    ma_nguoi_dung = %s
                WHERE ma_don_hang = %s
            """
            cursor.execute(order_query, (ngay_dat, tong_tien, ma_nguoi_dung, ma_don_hang))
            
            # Update order details
            details_query = """
                UPDATE CHITIETDONHANG
                SET so_luong = %s,
                    ma_san_pham = %s,
                    don_gia = %s
                WHERE ma_don_hang = %s
            """
            cursor.execute(details_query, (so_luong, ma_san_pham, don_gia, ma_don_hang))
            
            # Commit changes
            self.conn.commit()
            return True
            
        except Exception as e:
            # Rollback in case of error
            self.conn.rollback()
            print(f"Lỗi khi cập nhật đơn hàng: {e}")
            return False
        finally:
            if cursor:
                cursor.close() 