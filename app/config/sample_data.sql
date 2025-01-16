-- Insert roles
-- INSERT INTO user_roles (role_name, description) VALUES
-- ('administrator', 'Full access to all system features'),
-- ('registered_user', 'Wait for approval'),
-- ('user', 'View only'),
-- ('manager', 'Rights to manage all except users');

-- -- Insert users
-- INSERT INTO users (username, password, fullName, role_id) VALUES
-- ('manager1', '$2b$12$KIXQ1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1', 'Manager One', 4),
-- ('user1', '$2b$12$KIXQ1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1e1G1J1Q1', 'User One', 3);

-- -- Insert categories
-- INSERT INTO categories (name, description) VALUES
-- ('Electronics', 'Devices and gadgets'),
-- ('Furniture', 'Home and office furniture'),
-- ('Clothing', 'Apparel and accessories');

-- -- Insert suppliers
-- INSERT INTO suppliers (name, email, phone, address) VALUES
-- ('Tech Supplies Co.', 'contact@techsupplies.com', '123-456-7890', '123 Tech Lane'),
-- ('Furniture World', 'info@furnitureworld.com', '987-654-3210', '456 Furniture Ave'),
-- ('Fashion Hub', 'support@fashionhub.com', '555-123-4567', '789 Fashion Blvd');

-- -- Insert products
-- INSERT INTO products (name, description, category_id, supplier_id, unit_price) VALUES
-- ('Smartphone', 'Latest model smartphone', 1, 1, 699.99),
-- ('Office Chair', 'Ergonomic office chair', 2, 2, 149.99),
-- ('T-shirt', 'Cotton t-shirt', 3, 3, 19.99);

-- -- Insert inventory
-- INSERT INTO inventory (product_id, quantity, last_restock_date) VALUES
-- (1, 50, '2023-10-01'),
-- (2, 20, '2023-10-02'),
-- (3, 100, '2023-10-03');

-- -- Insert orders
-- INSERT INTO orders (user_id, order_date, total_amount) VALUES
-- (1, '2023-10-01', 150.00),
-- (1, '2023-10-02', 200.00),
-- (1, '2023-10-03', 300.00);

-- -- Insert order details
-- INSERT INTO order_details (order_id, product_id, quantity, unit_price) VALUES
-- (1, 1, 1, 699.99),
-- (2, 2, 2, 149.99),
-- (3, 3, 5, 19.99); 