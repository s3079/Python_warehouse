import customtkinter as ctk
from PIL import Image
from pathlib import Path
import tkinter as tk
from app.controllers.product_controller import ProductController
from app.views.admin.dialogs.product_dialog import ProductDialog
from app.views.admin.dialogs.center_dialog import CenterDialog

class ProductsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = ProductController()
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""
        
        # Load icons
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'search.png')),
            size=(20, 20)
        )
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'filter.png')),
            size=(20, 20)
        )
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'plus.png')),
            size=(20, 20)
        )
        self.trash_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'trash.png')),
            size=(16, 16)
        )
        self.edit_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'edit.png')),
            size=(16, 16)
        )
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-left.png')),
            size=(20, 20)
        )
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-right.png')),
            size=(20, 20)
        )

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section with search and buttons
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        
        # Create search frame
        search_frame = ctk.CTkFrame(
            top_section,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        search_frame.grid(row=0, column=0, sticky="w")
        
        # Add search icon and entry
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search products...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.on_search)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add filter button
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Filter",
            image=self.filter_icon,
            compound="left",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=45,
            corner_radius=8,
            command=self.show_filter_dialog
        )
        filter_button.pack(side="left", padx=(0, 10))
        
        # Add new product button
        new_product_button = ctk.CTkButton(
            buttons_frame,
            text="Add Product",
            image=self.plus_icon,
            compound="left",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,
            height=45,
            corner_radius=8,
            command=self.show_add_dialog
        )
        new_product_button.pack(side="left")
        
        # Create table container
        table_container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for table
        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Define column configurations
        self.columns = [
            {"name": "Name", "key": "name", "width": 100},
            {"name": "Description", "key": "description", "width": 150},
            {"name": "Category", "key": "category_name", "width": 150},
            {"name": "Supplier", "key": "supplier_name", "width": 100},
            {"name": "Price", "key": "unit_price", "width": 150},
            {"name": "Actions", "key": "actions", "width": 100}
        ]
        
        # Create table header
        header_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.pack(fill="x", expand=True)
        header_frame.pack_propagate(False)
        
        # Add header labels
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col["name"],
                font=("", 13, "bold"),
                text_color="#16151C",
                anchor="w",
                width=col["width"]
            )
            label.grid(row=0, column=i, padx=(20 if i == 0 else 10, 10), pady=15, sticky="w")
            
        # Create frame for table content
        self.content_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True)
        
        # Load initial data
        self.load_products()
    
    def on_search(self, event=None):
        """Handle search when Enter is pressed"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_products()

    def load_products(self):
        """Load products into the table"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Calculate pagination
        offset = (self.current_page - 1) * self.items_per_page
        
        # Get products from controller with pagination
        products, total_count = self.controller.get_products_paginated(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)  # Ceiling division
        
        # Configure grid columns for content frame
        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
        
        # Create rows for each product
        for i, product in enumerate(products):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            # Add product data
            for j, col in enumerate(self.columns):
                if col["key"] == "actions":
                    # Create actions frame
                    actions_frame = ctk.CTkFrame(
                        row_frame,
                        fg_color="transparent"
                    )
                    actions_frame.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                    # Edit button
                    edit_btn = ctk.CTkButton(
                        actions_frame,
                        text="",
                        image=self.edit_icon,
                        width=30,
                        height=30,
                        fg_color="#006EC4",
                        text_color="white",
                        hover_color="#0059A1",
                        command=lambda p=product: self.show_edit_dialog(p)
                    )
                    edit_btn.pack(side="left", padx=(0, 5))
                    
                    # Delete button
                    delete_btn = ctk.CTkButton(
                        actions_frame,
                        text="",
                        image=self.trash_icon,
                        width=30,
                        height=30,
                        fg_color="#e03137",
                        text_color="white",
                        hover_color="#b32429",
                        command=lambda p=product: self.delete_product(p)
                    )
                    delete_btn.pack(side="left")
                    
                elif col["key"] == "unit_price":
                    # Format price with currency
                    value = f"${float(product[col['key']]):.2f}"
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                else:
                    # Regular text columns
                    value = str(product.get(col["key"], "") or "")
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
            
            # Add separator
            separator = ctk.CTkFrame(
                self.content_frame,
                fg_color="#E5E5E5",
                height=1
            )
            separator.pack(fill="x")

        # Add pagination controls at the bottom
        self.create_pagination_controls(total_pages)

    def create_pagination_controls(self, total_pages):
        """Create pagination controls"""
        # Create or clear pagination frame
        if hasattr(self, 'pagination_frame'):
            for widget in self.pagination_frame.winfo_children():
                widget.destroy()
        else:
            self.pagination_frame = ctk.CTkFrame(self, fg_color="white", height=60)
            self.pagination_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
            self.pagination_frame.grid_propagate(False)
        
        # Create container for pagination elements
        controls_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        controls_frame.pack(expand=True, fill="both")
        
        # Left side - showing entries info
        left_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(start_index + self.items_per_page - 1, self.total_items)
        
        showing_label = ctk.CTkLabel(
            left_frame,
            text=f"Showing {start_index}-{end_index} of {self.total_items} entries",
            text_color="#6F6E77"
        )
        showing_label.pack(side="left")
        
        # Right side - pagination buttons
        right_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        # Previous page button
        prev_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_left_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.current_page > 1 else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.previous_page if self.current_page > 1 else None
        )
        prev_button.pack(side="left", padx=(0, 5))
        
        # Page number buttons
        visible_pages = 5
        start_page = max(1, min(self.current_page - visible_pages // 2,
                               total_pages - visible_pages + 1))
        end_page = min(start_page + visible_pages - 1, total_pages)
        
        for page in range(start_page, end_page + 1):
            is_current = page == self.current_page
            page_button = ctk.CTkButton(
                right_frame,
                text=str(page),
                width=30,
                height=30,
                fg_color="#006EC4" if is_current else "#F8F9FA",
                text_color="white" if is_current else "#16151C",
                hover_color="#0059A1" if is_current else "#E8E9EA",
                command=lambda p=page: self.go_to_page(p)
            )
            page_button.pack(side="left", padx=2)
        
        # Next page button
        next_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_right_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.current_page < total_pages else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.next_page if self.current_page < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_products()

    def next_page(self):
        """Go to next page"""
        self.current_page += 1
        self.load_products()

    def go_to_page(self, page):
        """Go to specific page"""
        self.current_page = page
        self.load_products()

    def show_add_dialog(self):
        """Show dialog to add a new product"""
        dialog = ProductDialog(
            self,
            on_save=self.save_product
        )

    def show_edit_dialog(self, product):
        """Show dialog to edit a product"""
        dialog = CenterDialog(self, "Edit Product","500X800")
        
        # Create main content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent",)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product name
        name_label = ctk.CTkLabel(
            content_frame,
            text="Name",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter product name",
            height=40,
            width=400
        )
        name_entry.pack(fill="x", pady=(0, 15))
        name_entry.insert(0, product["name"])
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text="Description",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        desc_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter product description",
            height=40,
            width=400
        )
        desc_entry.pack(fill="x", pady=(0, 15))
        desc_entry.insert(0, product["description"] if product["description"] else "")

        # Category
        category_label = ctk.CTkLabel(
            content_frame,
            text="Category",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        category_label.pack(anchor="w", pady=(0, 5))

        # Get categories from controller
        from app.controllers.category_controller import CategoryController
        category_controller = CategoryController()
        categories = category_controller.get_all_categories()
        category_names = [cat["name"] for cat in categories]
        
        category_combobox = ctk.CTkOptionMenu(
            content_frame,
            values=category_names,
            height=40,
            width=400,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        category_combobox.pack(fill="x", pady=(0, 15))
        category_combobox.set(product["category_name"] if product["category_name"] else "Select Category")

        # Supplier
        supplier_label = ctk.CTkLabel(
            content_frame,
            text="Supplier",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        supplier_label.pack(anchor="w", pady=(0, 5))

        # Get suppliers from controller
        from app.controllers.supplier_controller import SupplierController
        supplier_controller = SupplierController()
        suppliers = supplier_controller.get_all_suppliers()
        supplier_names = [sup["name"] for sup in suppliers]
        
        supplier_combobox = ctk.CTkOptionMenu(
            content_frame,
            values=supplier_names,
            height=40,
            width=400,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        supplier_combobox.pack(fill="x", pady=(0, 15))
        supplier_combobox.set(product["supplier_name"] if product["supplier_name"] else "Select Supplier")
        
        # Price
        price_label = ctk.CTkLabel(
            content_frame,
            text="Price",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        price_label.pack(anchor="w", pady=(0, 5))
        
        price_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter product price",
            height=40,
            width=400
        )
        price_entry.pack(fill="x", pady=(0, 15))
        price_entry.insert(0, str(product["unit_price"]))
        
        # Add buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.save_product_changes(
                dialog,
                product["product_id"],
                name_entry.get(),
                desc_entry.get(),
                price_entry.get(),
                category_combobox.get(),
                supplier_combobox.get()
            )
        )
        save_button.pack(side="left")

    def delete_product(self, product):
        """Show confirmation dialog and delete product"""
        dialog = CenterDialog(self, "Delete Product")
        
        # Create content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon or text
        warning_label = ctk.CTkLabel(
            content_frame,
            text="⚠️ Warning",
            font=("", 16, "bold"),
            text_color="#e03137"
        )
        warning_label.pack(pady=(0, 10))
        
        # Confirmation message
        message_label = ctk.CTkLabel(
            content_frame,
            text=f"Are you sure you want to delete '{product['name']}'?\nThis action cannot be undone.",
            font=("", 13),
            text_color="#16151C"
        )
        message_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Delete button
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.confirm_delete(dialog, product)
        )
        delete_button.pack(side="left")

    def save_product_changes(self, dialog, product_id, name, description, price, category_name, supplier_name):
        """Save product changes and close dialog"""
        try:
            # Validate inputs
            if not name:
                raise ValueError("Product name is required")
            if not category_name or category_name == "Select Category":
                raise ValueError("Category is required")
            if not supplier_name or supplier_name == "Select Supplier":
                raise ValueError("Supplier is required")
            try:
                price = float(price)
            except ValueError:
                raise ValueError("Price must be a valid number")
            
            # Get category_id from category_name
            from app.controllers.category_controller import CategoryController
            category_controller = CategoryController()
            categories = category_controller.get_all_categories()
            category = next((cat for cat in categories if cat["name"] == category_name), None)
            if not category:
                raise ValueError("Invalid category selected")

            # Get supplier_id from supplier_name
            from app.controllers.supplier_controller import SupplierController
            supplier_controller = SupplierController()
            suppliers = supplier_controller.get_all_suppliers()
            supplier = next((sup for sup in suppliers if sup["name"] == supplier_name), None)
            if not supplier:
                raise ValueError("Invalid supplier selected")
            
            # Update product
            success = self.controller.update_product(product_id, {
                "name": name,
                "description": description,
                "unit_price": price,
                "category_id": category["category_id"],
                "supplier_id": supplier["supplier_id"]
            })
            
            if success:
                dialog.destroy()
                self.load_products()  # Refresh the list
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to update product")
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))

    def confirm_delete(self, dialog, product):
        """Execute delete operation and close dialog"""
        try:
            if self.controller.delete_product(product["product_id"]):
                dialog.destroy()
                self.load_products()  # Refresh the list
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to delete product")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))

    def show_filter_dialog(self):
        """Show filter options dialog"""
        dialog = CenterDialog(self, "Filter Products", "400x300")
        
        # Store filter states
        self.name_sort = tk.StringVar(value="none")  # none, asc, desc
        self.price_sort = tk.StringVar(value="none")  # none, asc, desc
        
        # Create main content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name filter section
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Name",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
        # Name radio buttons
        name_options_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_options_frame.pack(fill="x")
        
        name_all = ctk.CTkRadioButton(
            name_options_frame,
            text="All",
            variable=self.name_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        name_all.pack(side="left", padx=(0, 15))
        
        name_asc = ctk.CTkRadioButton(
            name_options_frame,
            text="A-Z",
            variable=self.name_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        name_asc.pack(side="left", padx=(0, 15))
        
        name_desc = ctk.CTkRadioButton(
            name_options_frame,
            text="Z-A",
            variable=self.name_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        name_desc.pack(side="left")
        
        # Price filter section
        price_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=(0, 20))
        
        price_label = ctk.CTkLabel(
            price_frame,
            text="Price",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        price_label.pack(anchor="w", pady=(0, 10))
        
        # Price radio buttons
        price_options_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_options_frame.pack(fill="x")
        
        price_all = ctk.CTkRadioButton(
            price_options_frame,
            text="All",
            variable=self.price_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        price_all.pack(side="left", padx=(0, 15))
        
        price_asc = ctk.CTkRadioButton(
            price_options_frame,
            text="Low to High",
            variable=self.price_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        price_asc.pack(side="left", padx=(0, 15))
        
        price_desc = ctk.CTkRadioButton(
            price_options_frame,
            text="High to Low",
            variable=self.price_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        price_desc.pack(side="left")
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Apply button
        apply_button = ctk.CTkButton(
            buttons_frame,
            text="Apply",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.apply_filters(dialog)
        )
        apply_button.pack(side="left")

    def apply_filters(self, dialog):
        """Apply the selected filters and refresh the table"""
        dialog.destroy()
        self.current_page = 1  # Reset to first page
        self.load_products()

    def save_product(self, data):
        """Save or update product"""
        try:
            # Validate price format and range
            try:
                price = float(data['unit_price'])
                if price < 0 or price > 999999.99:  # Adjust max value based on your database decimal(10,2) limits
                    raise ValueError("Price must be between 0 and 999,999.99")
                # Format to 2 decimal places
                price = round(price, 2)
            except ValueError as e:
                if "must be between" in str(e):
                    raise e
                raise ValueError("Price must be a valid number")

            # Map the dialog data to match the controller's expected format
            product_data = {
                'name': data['name'],
                'description': data['description'],
                'unit_price': price,  # Use the validated and formatted price
                'category_id': None,  # We'll get this from the category name
                'supplier_id': None   # We'll get this from the supplier name
            }

            # Get category_id from category_name
            from app.controllers.category_controller import CategoryController
            category_controller = CategoryController()
            categories = category_controller.get_all_categories()
            category = next((cat for cat in categories if cat["name"] == data['category_name']), None)
            if category:
                product_data['category_id'] = category['category_id']
            else:
                raise ValueError("Invalid category selected")

            # Get supplier_id from supplier_name
            from app.controllers.supplier_controller import SupplierController
            supplier_controller = SupplierController()
            suppliers = supplier_controller.get_all_suppliers()
            supplier = next((sup for sup in suppliers if sup["name"] == data['supplier_name']), None)
            if supplier:
                product_data['supplier_id'] = supplier['supplier_id']
            else:
                raise ValueError("Invalid supplier selected")

            if "product_id" in data:
                # Update existing product
                success = self.controller.update_product(data["product_id"], product_data)
            else:
                # Add new product
                success = self.controller.add_product(product_data)
            
            if success:
                self.load_products()  # Refresh the products list
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to save product")
            
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to save product: {str(e)}")
