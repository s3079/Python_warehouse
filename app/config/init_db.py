import mysql.connector
from mysql.connector import Error
import os
from app.config.config import Config

def init_database():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        if conn.is_connected():
            cursor = conn.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            print(f"Cơ sở dữ liệu '{Config.DB_NAME}' đã được tạo hoặc đã tồn tại.")

            cursor.execute(f"USE {Config.DB_NAME}")

            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.join(current_dir, 'schema.sql')

            with open(schema_path, 'r') as schema_file:
                schema_script = schema_file.read()
                statements = schema_script.split(';')
            
                for statement in statements:
                    if statement.strip():
                        try:
                            cursor.execute(statement)
                        except Error as e:
                            print(f"Error executing statement: {e}")
                conn.commit()
            print("Cấu trúc cơ sở dữ liệu đã được tạo thành công.")

            cursor.execute("SELECT COUNT(*) FROM NGUOIDUNG")
            user_count = cursor.fetchone()[0]

            if user_count == 0:
                sample_data_path = os.path.join(current_dir, 'sample_data.sql')
                with open(sample_data_path, 'r') as sample_file:
                    sample_script = sample_file.read()
                    statements = sample_script.split(';')
                
                    for statement in statements:
                        if statement.strip():
                            try:
                                cursor.execute(statement)
                            except Error as e:
                                print(f"Error executing statement: {e}")
                    conn.commit()
                print("Dữ liệu mẫu đã được chèn thành công.")
            else:
                print("Đã có dữ liệu trong cơ sở dữ liệu, bỏ qua việc chèn dữ liệu mẫu.")

            cursor.execute("SELECT ma_nguoi_dung FROM NGUOIDUNG WHERE ten_dang_nhap = 'admin'")
            admin_exists = cursor.fetchone()
            
            if not admin_exists:
                cursor.execute("SELECT ma_quyen FROM PHANQUYEN WHERE ten_quyen = 'administrator'")
                admin_role = cursor.fetchone()
                
                if admin_role:
                    password = "admin@123"
                    cursor.execute("""
                        INSERT INTO NGUOIDUNG (ten_dang_nhap, mat_khau, ho_ten, ma_quyen)
                        VALUES (%s, %s, %s, %s)
                    """, ('admin', password, 'Quản trị viên', admin_role[0]))
                    conn.commit()
                    print("Tài khoản quản trị viên đã được tạo thành công.")
            else:
                print("Tài khoản quản trị viên đã tồn tại.")
                
    except Error as e:
        print(f"Lỗi: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_database()
