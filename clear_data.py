from database import Database

def clear_data():
    db = Database()
    db.connect()
    
    # Disable foreign key checks temporarily
    db.execute_query("SET FOREIGN_KEY_CHECKS = 0")
    
    # Clear all tables
    tables = ['inventory', 'order_details', 'orders', 'products', 'categories', 'suppliers']
    for table in tables:
        db.execute_query(f"TRUNCATE TABLE {table}")
    
    # Re-enable foreign key checks
    db.execute_query("SET FOREIGN_KEY_CHECKS = 1")
    
    db.disconnect()
    print("All data cleared successfully!")

if __name__ == "__main__":
    clear_data()
