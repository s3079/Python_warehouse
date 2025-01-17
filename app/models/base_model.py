from abc import ABC, abstractmethod
import mysql.connector
from app.config.config import Config

class BaseModel(ABC):
    
    def __init__(self):
        """
        + Input: Không có
        + Output: Khởi tạo đối tượng BaseModel với kết nối database
        """
        self.config = Config.get_db_config()
        self._ketNoi()

    def _ketNoi(self):
        """
        + Input: Không có
        + Output: Đối tượng kết nối database mới
        + Raises:
            - Exception khi không thể tạo kết nối database
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            # Use dictionary cursor by default
            self.conn.cursor_class = mysql.connector.cursor.MySQLCursorDict
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            self.conn = None
    
    def __del__(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects: Đóng kết nối database hiện tại nếu có
        """
        try:
            if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
                self.conn.close()
        except:
            pass  # Ignore errors during cleanup
    
    def _thucThiTruyVan(self, query, params=None):
        """
        + Input:
            - query: Câu truy vấn SQL cần thực thi
            - params: Tham số cho câu truy vấn (mặc định: None)
        + Output: 
            - SELECT: Danh sách kết quả truy vấn
            - INSERT/UPDATE/DELETE: Số dòng bị ảnh hưởng
        + Raises:
            - Exception khi thực thi truy vấn thất bại
        """
        cursor = None
        try:
            if not self.conn or not self.conn.is_connected():
                self._ketNoi()
            
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            
            self.conn.commit()
            return cursor
            
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def layTatCa(self):
        """Get all records"""
        pass
    
    def them(self, data):
        """Add a new record"""
        pass
    
    def capNhat(self, id, data):
        """Update a record"""
        pass
    
    def xoa(self, id):
        """Delete a record"""
        pass
