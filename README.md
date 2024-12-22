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

## Initial Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate     # On Windows
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Database Setup:
   - Install and start MySQL Server
   - Create a database named `warehouse`:
     ```sql
     CREATE DATABASE warehouse;
     ```
   - Import the schema:
     ```bash
     mysql -u your_username -p warehouse < schema.sql
     ```
   - (Optional) Load sample data:
     ```bash
     python sample_data.py
     ```

4. Configure Database Connection:
   - Open `database.py`
   - Update the connection settings:
     ```python
     host="localhost"
     user="your_username"
     password="your_password"
     database="warehouse"
     ```

## Running the Application

1. Start the application:
   ```bash
   python main.py
   ```

2. The main window will open with multiple tabs for different functionalities.

## Detailed Usage Guide

### Products Management
1. Click on the "Products" tab
2. To add a new product:
   - Click "Add New"
   - Fill in required fields (Name, Price, Category, etc.)
   - Click "Save"
3. To edit a product:
   - Select a product from the list
   - Click "Edit"
   - Modify the fields
   - Click "Save"
4. To delete a product:
   - Select a product
   - Click "Delete"
   - Confirm deletion

### Categories Management
1. Navigate to "Categories" tab
2. Add new category:
   - Enter category name
   - Click "Add"
3. Edit category:
   - Select category
   - Click "Edit"
   - Update name
   - Save changes
4. Delete category:
   - Select category
   - Click "Delete"
   - Confirm deletion

### Suppliers Management
1. Go to "Suppliers" tab
2. Add new supplier:
   - Fill in supplier details (Name, Contact, Address)
   - Click "Add"
3. Edit supplier information:
   - Select supplier
   - Click "Edit"
   - Update fields
   - Save changes

### Inventory Management
1. Access "Inventory" tab
2. View current stock levels
3. Update inventory:
   - Select product
   - Enter new quantity
   - Click "Update"
4. Check low stock alerts
5. View inventory history

### Data Management
- Use `clear_data.py` to reset the database (caution: this will delete all data)
- Use `init_db.py` to reinitialize the database structure
- Use `sample_data.py` to load sample data for testing

## Troubleshooting

1. Database Connection Issues:
   - Verify MySQL server is running
   - Check connection credentials in `database.py`
   - Ensure database `warehouse` exists

2. Package Installation Issues:
   - Verify Python version (3.x required)
   - Ensure pip is up to date
   - Try reinstalling requirements:
     ```bash
     pip install --upgrade -r requirements.txt
     ```

3. GUI Issues:
   - Ensure Tkinter is properly installed
   - Check system requirements
   - Verify screen resolution settings

## Support

For issues and feature requests, please contact the development team.

## Data Validation

The application includes validation for:
- Required fields
- Numeric values (price, quantity)
- Data format validation
- Warning messages for invalid inputs
