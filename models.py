from database import Database

class Model:
    def __init__(self):
        self.db = Database()
        
class CategoryModel(Model):
    def get_all(self):
        self.db.connect()
        result = self.db.execute_query("SELECT * FROM categories ORDER BY name")
        self.db.disconnect()
        return result
        
    def add(self, name, description):
        self.db.connect()
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        result = self.db.execute_query(query, (name, description))
        self.db.disconnect()
        return result
        
    def update(self, category_id, name, description):
        self.db.connect()
        query = "UPDATE categories SET name = %s, description = %s WHERE category_id = %s"
        result = self.db.execute_query(query, (name, description, category_id))
        self.db.disconnect()
        return result
        
    def delete(self, category_id):
        self.db.connect()
        query = "DELETE FROM categories WHERE category_id = %s"
        result = self.db.execute_query(query, (category_id,))
        self.db.disconnect()
        return result

class SupplierModel(Model):
    def get_all(self):
        self.db.connect()
        result = self.db.execute_query("SELECT * FROM suppliers ORDER BY name")
        self.db.disconnect()
        return result
        
    def add(self, name, contact_name, address, phone, email):
        self.db.connect()
        query = "INSERT INTO suppliers (name, contact_name, address, phone, email) VALUES (%s, %s, %s, %s, %s)"
        result = self.db.execute_query(query, (name, contact_name, address, phone, email))
        self.db.disconnect()
        return result
        
    def update(self, supplier_id, name, contact_name, address, phone, email):
        self.db.connect()
        query = """UPDATE suppliers 
                  SET name = %s, contact_name = %s, address = %s, phone = %s, email = %s 
                  WHERE supplier_id = %s"""
        result = self.db.execute_query(query, (name, contact_name, address, phone, email, supplier_id))
        self.db.disconnect()
        return result
        
    def delete(self, supplier_id):
        self.db.connect()
        query = "DELETE FROM suppliers WHERE supplier_id = %s"
        result = self.db.execute_query(query, (supplier_id,))
        self.db.disconnect()
        return result

class ProductModel(Model):
    def get_all(self):
        self.db.connect()
        query = """SELECT p.*, c.name as category_name, s.name as supplier_name 
                  FROM products p 
                  LEFT JOIN categories c ON p.category_id = c.category_id 
                  LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                  ORDER BY p.name"""
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result
        
    def add(self, name, description, price, category_id, supplier_id):
        self.db.connect()
        query = """INSERT INTO products 
                  (name, description, price, category_id, supplier_id) 
                  VALUES (%s, %s, %s, %s, %s)"""
        result = self.db.execute_query(query, (name, description, price, category_id, supplier_id))
        self.db.disconnect()
        return result
        
    def update(self, product_id, name, description, price, category_id, supplier_id):
        self.db.connect()
        query = """UPDATE products 
                  SET name = %s, description = %s, price = %s, 
                      category_id = %s, supplier_id = %s 
                  WHERE product_id = %s"""
        result = self.db.execute_query(query, 
                                     (name, description, price, category_id, supplier_id, product_id))
        self.db.disconnect()
        return result
        
    def delete(self, product_id):
        self.db.connect()
        query = "DELETE FROM products WHERE product_id = %s"
        result = self.db.execute_query(query, (product_id,))
        self.db.disconnect()
        return result

class InventoryModel(Model):
    def get_all(self):
        self.db.connect()
        query = """SELECT i.*, p.name as product_name 
                  FROM inventory i 
                  JOIN products p ON i.product_id = p.product_id
                  ORDER BY p.name"""
        result = self.db.execute_query(query)
        self.db.disconnect()
        return result
        
    def update_quantity(self, product_id, quantity):
        self.db.connect()
        query = """INSERT INTO inventory (product_id, quantity) 
                  VALUES (%s, %s) 
                  ON DUPLICATE KEY UPDATE quantity = %s"""
        result = self.db.execute_query(query, (product_id, quantity, quantity))
        self.db.disconnect()
        return result
