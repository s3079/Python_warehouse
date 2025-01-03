import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from app.config.config import Config

def init_database():
    # First, create database if it doesn't exist
    try:
        # Connect without database name first
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            print(f"Database '{Config.DB_NAME}' created or already exists.")
            
            # Switch to the database
            cursor.execute(f"USE {Config.DB_NAME}")
            
            # Get the absolute path to schema.sql
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.join(current_dir, 'schema.sql')
            
            # Read and execute schema.sql
            with open(schema_path, 'r') as schema_file:
                schema_script = schema_file.read()
                # Split the script into individual statements
                statements = schema_script.split(';')
                
                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)
                conn.commit()
            print("Database schema created successfully.")
            
            # Create admin user if it doesn't exist
            # First check if admin exists
            cursor.execute("SELECT user_id FROM users WHERE username = 'admin'")
            admin_exists = cursor.fetchone()
            
            if not admin_exists:
                # Get admin role id
                cursor.execute("SELECT role_id FROM user_roles WHERE role_name = 'administrator'")
                admin_role = cursor.fetchone()
                
                if admin_role:
                    # Hash the password
                    password = "admin@123"
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    # Create admin user
                    cursor.execute("""
                        INSERT INTO users (username, password, email, role_id)
                        VALUES (%s, %s, %s, %s)
                    """, ('admin', hashed_password, 'admin@warehouse.com', admin_role[0]))
                    conn.commit()
                    print("Admin account created successfully.")
                else:
                    print("Error: Administrator role not found.")
            else:
                print("Admin account already exists.")
                
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_database()
