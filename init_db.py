import mysql.connector
from mysql.connector import Error

def init_database():
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            user="root",
            password="LeeNghien97@"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS warehouse")
            cursor.execute("USE warehouse")
            
            # Read and execute the SQL script
            with open('schema.sql', 'r') as file:
                sql_script = file.read()
                
            # Split and execute each statement
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement + ';')
                    
            connection.commit()
            print("Database initialized successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_database()
