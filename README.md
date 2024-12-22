# Warehouse Management System

A Python-based Warehouse Management System with a Tkinter GUI interface and MySQL database.

## Features

- Product Management (CRUD operations)
- Category Management
- Supplier Management
- Inventory Tracking
- Data validation
- User-friendly interface

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages (install using `pip install -r requirements.txt`):
  - mysql-connector-python
  - tkcalendar

## Database Setup

1. Create a MySQL database named `warehouse`
2. Import the provided SQL schema
3. Update the database connection settings in `database.py`:
   - host
   - user
   - password
   - database name

## Running the Application

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main application:
   ```bash
   python main.py
   ```

## Usage

The application provides four main tabs:

1. Products
   - Add, update, and delete products
   - View product list
   - Set product details (name, description, price)

2. Categories
   - Manage product categories
   - Add, update, and delete categories
   - View category list

3. Suppliers
   - Manage supplier information
   - Add, update, and delete suppliers
   - View supplier list

4. Inventory
   - Track product quantities
   - Update inventory levels
   - View current stock

## Data Validation

The application includes validation for:
- Required fields
- Numeric values (price, quantity)
- Data format validation
- Warning messages for invalid inputs
