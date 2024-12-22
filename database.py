import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.user = "root"
        self.password = "LeeNghien97@"  # Set your MySQL password here
        self.database = "warehouse"
        self.connection = None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return False
            
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.commit()
                return cursor.lastrowid
            else:
                result = cursor.fetchall()
                return result if result else []
        except Error as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            cursor.close()
