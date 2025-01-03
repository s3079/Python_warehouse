import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import mysql.connector
from app.config.config import Config
import os

def reset_database():
    """Reset the database to its initial state"""
    # Get database configuration
    config = Config.get_db_config()
    
    # Create connection without database
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password']
    )
    
    cursor = conn.cursor()
    
    try:
        # Drop database if exists
        cursor.execute(f"DROP DATABASE IF EXISTS {config['database']}")
        print(f"Dropped database {config['database']}")
        
        # Create database
        cursor.execute(f"CREATE DATABASE {config['database']}")
        print(f"Created database {config['database']}")
        
        # Use the database
        cursor.execute(f"USE {config['database']}")
        
        # Read and execute schema.sql
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 'app', 'config', 'schema.sql')
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            
        # Split and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("Schema created successfully")
        
        print("Database reset completed successfully")
        
    except Exception as e:
        print(f"Error resetting database: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    reset_database()
