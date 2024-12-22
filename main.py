import tkinter as tk
from tkinter import ttk, messagebox
from models import CategoryModel, SupplierModel, ProductModel, InventoryModel
from languages import LANGUAGES

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.current_language = 'English'
        self.setup_window()
        
    def setup_window(self):
        self.root.title(self.translate('app_title'))
        self.root.geometry("1200x800")
        
        # Initialize models
        self.category_model = CategoryModel()
        self.supplier_model = SupplierModel()
        self.product_model = ProductModel()
        self.inventory_model = InventoryModel()
        
        # Create language selector
        self.create_language_selector()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_products_tab()
        self.create_categories_tab()
        self.create_suppliers_tab()
        self.create_inventory_tab()
        
    def translate(self, key):
        return LANGUAGES[self.current_language][key]
        
    def create_language_selector(self):
        language_frame = ttk.Frame(self.root)
        language_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(language_frame, text=self.translate('language') + ":").pack(side='left', padx=5)
        self.language_var = tk.StringVar(value=self.current_language)
        language_combo = ttk.Combobox(language_frame, 
                                    textvariable=self.language_var,
                                    values=list(LANGUAGES.keys()),
                                    state='readonly',
                                    width=20)
        language_combo.pack(side='left')
        language_combo.bind('<<ComboboxSelected>>', self.change_language)
        
    def change_language(self, event=None):
        new_language = self.language_var.get()
        if new_language != self.current_language:
            self.current_language = new_language
            # Rebuild the interface with new language
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_window()
            
    def create_products_tab(self):
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text=self.translate('products_tab'))
        
        # Form Frame
        form_frame = ttk.LabelFrame(products_frame, text=self.translate('product_details'), padding=10)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Product Form
        ttk.Label(form_frame, text=self.translate('name')).grid(row=0, column=0, padx=5, pady=5)
        self.product_name = ttk.Entry(form_frame, width=40)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('description')).grid(row=1, column=0, padx=5, pady=5)
        self.product_desc = ttk.Entry(form_frame, width=40)
        self.product_desc.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('price')).grid(row=2, column=0, padx=5, pady=5)
        self.product_price = ttk.Entry(form_frame, width=40)
        self.product_price.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('category')).grid(row=3, column=0, padx=5, pady=5)
        self.product_category = ttk.Combobox(form_frame, width=37)
        self.product_category.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('supplier')).grid(row=4, column=0, padx=5, pady=5)
        self.product_supplier = ttk.Combobox(form_frame, width=37)
        self.product_supplier.grid(row=4, column=1, padx=5, pady=5)
        
        # Update comboboxes
        self.update_product_comboboxes()
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=f"{self.translate('add')} {self.translate('product')}", 
                  command=self.add_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('update')} {self.translate('product')}", 
                  command=self.update_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('delete')} {self.translate('product')}", 
                  command=self.delete_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.translate('clear'), 
                  command=self.clear_product_fields).pack(side='left', padx=5)
        
        # Treeview
        self.products_tree = ttk.Treeview(products_frame, 
                                        columns=('ID', 'Name', 'Description', 'Price', 'Category', 'Supplier'), 
                                        show='headings')
        self.products_tree.heading('ID', text=self.translate('id'))
        self.products_tree.heading('Name', text=self.translate('name'))
        self.products_tree.heading('Description', text=self.translate('description'))
        self.products_tree.heading('Price', text=self.translate('price'))
        self.products_tree.heading('Category', text=self.translate('category'))
        self.products_tree.heading('Supplier', text=self.translate('supplier'))
        
        # Configure column widths
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=150)
        self.products_tree.column('Description', width=200)
        self.products_tree.column('Price', width=100)
        self.products_tree.column('Category', width=150)
        self.products_tree.column('Supplier', width=150)
        
        self.products_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind select event
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Load products
        self.load_products()
        
    def create_categories_tab(self):
        categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(categories_frame, text=self.translate('categories_tab'))
        
        # Form Frame
        form_frame = ttk.LabelFrame(categories_frame, text=self.translate('category_details'), padding=10)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Category Form
        ttk.Label(form_frame, text=self.translate('name')).grid(row=0, column=0, padx=5, pady=5)
        self.category_name = ttk.Entry(form_frame, width=40)
        self.category_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('description')).grid(row=1, column=0, padx=5, pady=5)
        self.category_desc = ttk.Entry(form_frame, width=40)
        self.category_desc.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=f"{self.translate('add')} {self.translate('category')}", 
                  command=self.add_category).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('update')} {self.translate('category')}", 
                  command=self.update_category).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('delete')} {self.translate('category')}", 
                  command=self.delete_category).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.translate('clear'), 
                  command=self.clear_category_fields).pack(side='left', padx=5)
        
        # Treeview
        self.categories_tree = ttk.Treeview(categories_frame, 
                                          columns=('ID', 'Name', 'Description'), 
                                          show='headings')
        self.categories_tree.heading('ID', text=self.translate('id'))
        self.categories_tree.heading('Name', text=self.translate('name'))
        self.categories_tree.heading('Description', text=self.translate('description'))
        
        self.categories_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind select event
        self.categories_tree.bind('<<TreeviewSelect>>', self.on_category_select)
        
        # Load categories
        self.load_categories()
        
    def create_suppliers_tab(self):
        suppliers_frame = ttk.Frame(self.notebook)
        self.notebook.add(suppliers_frame, text=self.translate('suppliers_tab'))
        
        # Form Frame
        form_frame = ttk.LabelFrame(suppliers_frame, text=self.translate('supplier_details'), padding=10)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Supplier Form
        ttk.Label(form_frame, text=self.translate('name')).grid(row=0, column=0, padx=5, pady=5)
        self.supplier_name = ttk.Entry(form_frame, width=40)
        self.supplier_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('contact_name')).grid(row=1, column=0, padx=5, pady=5)
        self.supplier_contact = ttk.Entry(form_frame, width=40)
        self.supplier_contact.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('phone')).grid(row=2, column=0, padx=5, pady=5)
        self.supplier_phone = ttk.Entry(form_frame, width=40)
        self.supplier_phone.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('email')).grid(row=3, column=0, padx=5, pady=5)
        self.supplier_email = ttk.Entry(form_frame, width=40)
        self.supplier_email.grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=f"{self.translate('add')} {self.translate('supplier')}", 
                  command=self.add_supplier).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('update')} {self.translate('supplier')}", 
                  command=self.update_supplier).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=f"{self.translate('delete')} {self.translate('supplier')}", 
                  command=self.delete_supplier).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.translate('clear'), 
                  command=self.clear_supplier_fields).pack(side='left', padx=5)
        
        # Treeview
        self.suppliers_tree = ttk.Treeview(suppliers_frame, 
                                         columns=('ID', 'Name', 'Contact', 'Phone', 'Email'), 
                                         show='headings')
        self.suppliers_tree.heading('ID', text=self.translate('id'))
        self.suppliers_tree.heading('Name', text=self.translate('name'))
        self.suppliers_tree.heading('Contact', text=self.translate('contact_name'))
        self.suppliers_tree.heading('Phone', text=self.translate('phone'))
        self.suppliers_tree.heading('Email', text=self.translate('email'))
        
        self.suppliers_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind select event
        self.suppliers_tree.bind('<<TreeviewSelect>>', self.on_supplier_select)
        
        # Load suppliers
        self.load_suppliers()
        
    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text=self.translate('inventory_tab'))
        
        # Form Frame
        form_frame = ttk.LabelFrame(inventory_frame, text=self.translate('inventory_details'), padding=10)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Inventory Form
        ttk.Label(form_frame, text=self.translate('product')).grid(row=0, column=0, padx=5, pady=5)
        self.inventory_product = ttk.Combobox(form_frame, width=37)
        self.inventory_product.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self.translate('quantity')).grid(row=1, column=0, padx=5, pady=5)
        self.inventory_quantity = ttk.Entry(form_frame, width=40)
        self.inventory_quantity.grid(row=1, column=1, padx=5, pady=5)
        
        # Update product combobox
        self.update_inventory_product_combobox()
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=f"{self.translate('update')} {self.translate('inventory')}", 
                  command=self.update_inventory).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.translate('clear'), 
                  command=self.clear_inventory_fields).pack(side='left', padx=5)
        
        # Treeview
        self.inventory_tree = ttk.Treeview(inventory_frame, 
                                         columns=('ID', 'Product', 'Quantity', 'Last Updated'), 
                                         show='headings')
        self.inventory_tree.heading('ID', text=self.translate('id'))
        self.inventory_tree.heading('Product', text=self.translate('product'))
        self.inventory_tree.heading('Quantity', text=self.translate('quantity'))
        self.inventory_tree.heading('Last Updated', text=self.translate('last_updated'))
        
        self.inventory_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind select event
        self.inventory_tree.bind('<<TreeviewSelect>>', self.on_inventory_select)
        
        # Load inventory
        self.load_inventory()
        
    # Message methods
    def show_error(self, key, *args):
        messagebox.showerror("Error", self.translate(key).format(*args))
        
    def show_success(self, key, *args):
        messagebox.showinfo("Success", self.translate(key).format(*args))
        
    def show_warning(self, key, *args):
        messagebox.showwarning("Warning", self.translate(key).format(*args))
        
    def confirm_delete(self, item_type):
        return messagebox.askyesno("Confirm", self.translate('confirm_delete').format(self.translate(item_type)))
        
    def clear_product_fields(self):
        self.product_name.delete(0, tk.END)
        self.product_desc.delete(0, tk.END)
        self.product_price.delete(0, tk.END)
        self.product_category.set('')
        self.product_supplier.set('')
        
    def clear_category_fields(self):
        self.category_name.delete(0, tk.END)
        self.category_desc.delete(0, tk.END)
        
    def clear_supplier_fields(self):
        self.supplier_name.delete(0, tk.END)
        self.supplier_contact.delete(0, tk.END)
        self.supplier_phone.delete(0, tk.END)
        self.supplier_email.delete(0, tk.END)
        
    def clear_inventory_fields(self):
        self.inventory_product.set('')
        self.inventory_quantity.delete(0, tk.END)
        
    def update_product_comboboxes(self):
        # Update category combobox
        categories = self.category_model.get_all()
        self.category_names = {cat['name']: cat['category_id'] for cat in categories}
        self.product_category['values'] = list(self.category_names.keys())
        
        # Update supplier combobox
        suppliers = self.supplier_model.get_all()
        self.supplier_names = {sup['name']: sup['supplier_id'] for sup in suppliers}
        self.product_supplier['values'] = list(self.supplier_names.keys())
        
    def on_product_select(self, event):
        selected = self.products_tree.selection()
        if selected:
            item = self.products_tree.item(selected[0])
            values = item['values']
            
            self.clear_product_fields()
            self.product_name.insert(0, values[1])
            self.product_desc.insert(0, values[2])
            self.product_price.insert(0, values[3])
            self.product_category.set(values[4])
            self.product_supplier.set(values[5])
            
    def on_category_select(self, event):
        selected = self.categories_tree.selection()
        if selected:
            item = self.categories_tree.item(selected[0])
            values = item['values']
            
            self.clear_category_fields()
            self.category_name.insert(0, values[1])
            self.category_desc.insert(0, values[2])
            
    def on_supplier_select(self, event):
        selected = self.suppliers_tree.selection()
        if selected:
            item = self.suppliers_tree.item(selected[0])
            values = item['values']
            
            self.clear_supplier_fields()
            self.supplier_name.insert(0, values[1])
            self.supplier_contact.insert(0, values[2])
            self.supplier_phone.insert(0, values[3])
            self.supplier_email.insert(0, values[4])
            
    def on_inventory_select(self, event):
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected[0])
            values = item['values']
            
            self.clear_inventory_fields()
            self.inventory_product.set(values[1])
            self.inventory_quantity.insert(0, values[2])
            
    def update_inventory_product_combobox(self):
        products = self.product_model.get_all()
        self.product_ids = {prod['name']: prod['product_id'] for prod in products}
        self.inventory_product['values'] = list(self.product_ids.keys())
        
    def load_products(self):
        products = self.product_model.get_all()
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        for product in products:
            self.products_tree.insert('', 'end', values=(
                product['product_id'],
                product['name'],
                product['description'],
                product['price'],
                product.get('category_name', ''),
                product.get('supplier_name', '')
            ))
            
    def load_categories(self):
        categories = self.category_model.get_all()
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        for category in categories:
            self.categories_tree.insert('', 'end', values=(
                category['category_id'],
                category['name'],
                category['description']
            ))
            
    def load_suppliers(self):
        suppliers = self.supplier_model.get_all()
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        for supplier in suppliers:
            self.suppliers_tree.insert('', 'end', values=(
                supplier['supplier_id'],
                supplier['name'],
                supplier['contact_name'],
                supplier['phone'],
                supplier['email']
            ))
            
    def load_inventory(self):
        inventory = self.inventory_model.get_all()
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        for inv in inventory:
            self.inventory_tree.insert('', 'end', values=(
                inv['inventory_id'],
                inv['product_name'],
                inv['quantity'],
                inv['last_updated']
            ))
            
    def add_product(self):
        try:
            name = self.product_name.get()
            description = self.product_desc.get()
            price = float(self.product_price.get())
            category = self.product_category.get()
            supplier = self.product_supplier.get()
            
            if not name:
                self.show_error("product_name_required")
                return
                
            if price <= 0:
                self.show_error("price_must_be_greater_than_zero")
                return
                
            category_id = self.category_names.get(category)
            supplier_id = self.supplier_names.get(supplier)
            
            self.product_model.add(name, description, price, category_id, supplier_id)
            self.load_products()
            self.clear_product_fields()
            self.update_inventory_product_combobox()
            self.show_success("product_added_successfully")
            
        except ValueError:
            self.show_error("invalid_price_format")
            
    def update_product(self):
        selected = self.products_tree.selection()
        if not selected:
            self.show_warning("please_select_a_product_to_update")
            return
            
        try:
            product_id = self.products_tree.item(selected[0])['values'][0]
            name = self.product_name.get()
            description = self.product_desc.get()
            price = float(self.product_price.get())
            category = self.product_category.get()
            supplier = self.product_supplier.get()
            
            if not name:
                self.show_error("product_name_required")
                return
                
            if price <= 0:
                self.show_error("price_must_be_greater_than_zero")
                return
                
            category_id = self.category_names.get(category)
            supplier_id = self.supplier_names.get(supplier)
            
            self.product_model.update(product_id, name, description, price, category_id, supplier_id)
            self.load_products()
            self.clear_product_fields()
            self.show_success("product_updated_successfully")
            
        except ValueError:
            self.show_error("invalid_price_format")
            
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            self.show_warning("please_select_a_product_to_delete")
            return
            
        if self.confirm_delete("product"):
            product_id = self.products_tree.item(selected[0])['values'][0]
            self.product_model.delete(product_id)
            self.load_products()
            self.clear_product_fields()
            self.update_inventory_product_combobox()
            self.show_success("product_deleted_successfully")
            
    def add_category(self):
        name = self.category_name.get()
        description = self.category_desc.get()
        
        if not name:
            self.show_error("category_name_required")
            return
            
        self.category_model.add(name, description)
        self.load_categories()
        self.clear_category_fields()
        self.update_product_comboboxes()
        self.show_success("category_added_successfully")
        
    def update_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            self.show_warning("please_select_a_category_to_update")
            return
            
        category_id = self.categories_tree.item(selected[0])['values'][0]
        name = self.category_name.get()
        description = self.category_desc.get()
        
        if not name:
            self.show_error("category_name_required")
            return
            
        self.category_model.update(category_id, name, description)
        self.load_categories()
        self.clear_category_fields()
        self.update_product_comboboxes()
        self.load_products()  # Refresh products to update category names
        self.show_success("category_updated_successfully")
        
    def delete_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            self.show_warning("please_select_a_category_to_delete")
            return
            
        if self.confirm_delete("category"):
            category_id = self.categories_tree.item(selected[0])['values'][0]
            self.category_model.delete(category_id)
            self.load_categories()
            self.clear_category_fields()
            self.update_product_comboboxes()
            self.load_products()  # Refresh products to update category names
            self.show_success("category_deleted_successfully")
            
    def add_supplier(self):
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        phone = self.supplier_phone.get()
        email = self.supplier_email.get()
        
        if not name:
            self.show_error("supplier_name_required")
            return
            
        self.supplier_model.add(name, contact, "", phone, email)
        self.load_suppliers()
        self.clear_supplier_fields()
        self.update_product_comboboxes()
        self.show_success("supplier_added_successfully")
        
    def update_supplier(self):
        selected = self.suppliers_tree.selection()
        if not selected:
            self.show_warning("please_select_a_supplier_to_update")
            return
            
        supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        phone = self.supplier_phone.get()
        email = self.supplier_email.get()
        
        if not name:
            self.show_error("supplier_name_required")
            return
            
        self.supplier_model.update(supplier_id, name, contact, "", phone, email)
        self.load_suppliers()
        self.clear_supplier_fields()
        self.update_product_comboboxes()
        self.load_products()  # Refresh products to update supplier names
        self.show_success("supplier_updated_successfully")
        
    def delete_supplier(self):
        selected = self.suppliers_tree.selection()
        if not selected:
            self.show_warning("please_select_a_supplier_to_delete")
            return
            
        if self.confirm_delete("supplier"):
            supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
            self.supplier_model.delete(supplier_id)
            self.load_suppliers()
            self.clear_supplier_fields()
            self.update_product_comboboxes()
            self.load_products()  # Refresh products to update supplier names
            self.show_success("supplier_deleted_successfully")
            
    def update_inventory(self):
        try:
            product = self.inventory_product.get()
            quantity = int(self.inventory_quantity.get())
            
            if not product:
                self.show_error("please_select_a_product")
                return
                
            if quantity < 0:
                self.show_error("quantity_cannot_be_negative")
                return
                
            product_id = self.product_ids.get(product)
            if product_id:
                self.inventory_model.update_quantity(product_id, quantity)
                self.load_inventory()
                self.clear_inventory_fields()
                self.show_success("inventory_updated_successfully")
            else:
                self.show_error("invalid_product_selected")
                
        except ValueError:
            self.show_error("invalid_quantity_format")

if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
