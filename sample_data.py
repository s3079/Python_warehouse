from database import Database

def insert_sample_data():
    db = Database()
    db.connect()
    
    # Insert Categories
    categories = [
        ("Electronics", "Electronic devices and accessories"),
        ("Office Supplies", "Office stationery and supplies"),
        ("Furniture", "Office and home furniture"),
        ("Books", "Educational and reference books"),
        ("Sports Equipment", "Sports and fitness equipment")
    ]
    
    for name, description in categories:
        db.execute_query(
            "INSERT INTO categories (name, description) VALUES (%s, %s)",
            (name, description)
        )
    
    # Insert Suppliers
    suppliers = [
        ("TechCorp Inc.", "John Smith", "123 Tech Street, Silicon Valley", "408-555-1234", "john@techcorp.com"),
        ("Office Plus", "Mary Johnson", "456 Office Ave, Business District", "415-555-5678", "mary@officeplus.com"),
        ("Furniture World", "David Brown", "789 Furniture Blvd, Design District", "510-555-9012", "david@furnitureworld.com"),
        ("Book Haven", "Sarah Wilson", "321 Library Lane, Book District", "650-555-3456", "sarah@bookhaven.com"),
        ("Sports Elite", "Mike Thompson", "654 Sports Center, Athletic Zone", "925-555-7890", "mike@sportselite.com")
    ]
    
    for name, contact, address, phone, email in suppliers:
        db.execute_query(
            "INSERT INTO suppliers (name, contact_name, address, phone, email) VALUES (%s, %s, %s, %s, %s)",
            (name, contact, address, phone, email)
        )
    
    # Insert Products
    products = [
        ("Laptop Pro X", "High-performance laptop with 16GB RAM", 1299.99, 1, 1),
        ("Office Chair Deluxe", "Ergonomic office chair with lumbar support", 299.99, 3, 3),
        ("Premium Notebook", "High-quality notebook, 200 pages", 12.99, 2, 2),
        ("Python Programming Guide", "Comprehensive Python programming book", 49.99, 4, 4),
        ("Wireless Mouse", "Bluetooth wireless mouse", 29.99, 1, 1),
        ("Yoga Mat", "Premium non-slip yoga mat", 39.99, 5, 5),
        ("Desktop Monitor", "27-inch 4K monitor", 499.99, 1, 1),
        ("Filing Cabinet", "3-drawer metal filing cabinet", 149.99, 2, 2),
        ("Desk Lamp", "LED desk lamp with adjustable brightness", 34.99, 2, 2),
        ("Basketball", "Professional indoor/outdoor basketball", 29.99, 5, 5)
    ]
    
    for name, description, price, category_id, supplier_id in products:
        db.execute_query(
            "INSERT INTO products (name, description, price, category_id, supplier_id) VALUES (%s, %s, %s, %s, %s)",
            (name, description, price, category_id, supplier_id)
        )
    
    # Insert Inventory
    inventory = [
        (1, 50),  # Laptop Pro X
        (2, 30),  # Office Chair Deluxe
        (3, 200), # Premium Notebook
        (4, 100), # Python Programming Guide
        (5, 150), # Wireless Mouse
        (6, 75),  # Yoga Mat
        (7, 40),  # Desktop Monitor
        (8, 25),  # Filing Cabinet
        (9, 80),  # Desk Lamp
        (10, 60)  # Basketball
    ]
    
    for product_id, quantity in inventory:
        db.execute_query(
            "INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)",
            (product_id, quantity)
        )
    
    db.disconnect()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
