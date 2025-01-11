import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path
from app.controllers.inventory_controller import InventoryController
import math
import tkinter as tk

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = InventoryController()
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""  # Add search query variable 
        
        # Load icons
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        search_icon_path = str(assets_path / 'search.png')
        chevron_left_path = str(assets_path / 'chevron-left.png')
        chevron_right_path = str(assets_path / 'chevron-right.png')
        plus_icon_path = str(assets_path / 'plus.png')
        filter_icon_path = str(assets_path / 'filter.png')
        
        # Create all icons
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(search_icon_path),
            size=(20, 20)
        )
        
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(chevron_left_path),
            size=(20, 20)
        )
        
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(chevron_right_path),
            size=(20, 20)
        )
        
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(plus_icon_path),
            size=(20, 20)
        )
        
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(filter_icon_path),
            size=(20, 20)
        )
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section container
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
        
        # Add search icon
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        # Add search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search inventory...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", self.on_search)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add new inventory button
        new_inventory_button = ctk.CTkButton(
            buttons_frame,
            text="Add Inventory",
            image=self.plus_icon,
            compound="left",  # Places the icon to the left of the text
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,  # Increased width to accommodate icon
            height=45,
            corner_radius=8,
            command=self.show_add_dialog
        )
        new_inventory_button.pack(side="left", padx=(0, 10))  # Added right padding
        
        # Add filter button
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="",
            image=self.filter_icon,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#F0F0F0",
            width=45,
            height=45,
            corner_radius=8,
            command=self.show_filter_dialog
        )
        filter_button.pack(side="left")
        
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
        table_container.grid_rowconfigure(0, weight=1)  # Content area expands
        table_container.grid_rowconfigure(1, weight=0)  # Pagination stays at bottom

        # Create content area with fixed height for 10 rows
        content_frame = ctk.CTkFrame(
            table_container,
            fg_color="transparent",
            height=500  # Fixed height for 10 rows (10 * 50px)
        )
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.grid_propagate(False)  # Force fixed height
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Create scrollable frame inside content frame
        self.table_content = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            orientation="vertical"
        )
        self.table_content.grid(row=0, column=0, sticky="nsew")
        self.table_content.grid_columnconfigure(0, weight=1)

        # Create main frame to hold both header and content
        main_frame = ctk.CTkFrame(
            self.table_content,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True)
        
        # Set fixed minimum width for columns
        product_name_width = 200
        quantity_width = 100
        category_width = 150
        supplier_width = 150
        
        # Configure columns with weights and minimum sizes
        main_frame.grid_columnconfigure(0, weight=3, minsize=product_name_width)  # Product Name
        main_frame.grid_columnconfigure(1, weight=2, minsize=quantity_width)  # Quantity
        main_frame.grid_columnconfigure(2, weight=3, minsize=category_width)  # Category
        main_frame.grid_columnconfigure(3, weight=3, minsize=supplier_width)  # Supplier
        
        # Create header row with fixed height
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=1)
        header_frame.grid_propagate(False)  # Force fixed height

        # Configure header columns with same weights and minimum sizes
        header_frame.grid_columnconfigure(0, weight=3, minsize=product_name_width)  # Product Name
        header_frame.grid_columnconfigure(1, weight=2, minsize=quantity_width)  # Quantity
        header_frame.grid_columnconfigure(2, weight=3, minsize=category_width)  # Category
        header_frame.grid_columnconfigure(3, weight=3, minsize=supplier_width)  # Supplier
        header_frame.grid_propagate(False)

        # Add header labels with fixed widths
        product_name_header = ctk.CTkLabel(
            header_frame,
            text="Product Name",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=product_name_width
        )
        product_name_header.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

        quantity_header = ctk.CTkLabel(
            header_frame,
            text="Quantity",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=quantity_width
        )
        quantity_header.grid(row=0, column=1, padx=10, pady=15, sticky="w")

        category_header = ctk.CTkLabel(
            header_frame,
            text="Category",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=category_width
        )
        category_header.grid(row=0, column=2, padx=10, pady=15, sticky="w")

        supplier_header = ctk.CTkLabel(
            header_frame,
            text="Supplier",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=supplier_width
        )
        supplier_header.grid(row=0, column=3, padx=10, pady=15, sticky="w")
        
        # Create content frame
        self.main_content = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        self.main_content.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        # Configure column weights for content
        self.main_content.grid_columnconfigure(0, weight=3, minsize=product_name_width)  # Product Name
        self.main_content.grid_columnconfigure(1, weight=2, minsize=quantity_width)  # Quantity
        self.main_content.grid_columnconfigure(2, weight=3, minsize=category_width)  # Category
        self.main_content.grid_columnconfigure(3, weight=3, minsize=supplier_width)  # Supplier
        
        # Add pagination frame at the bottom with minimal height
        self.pagination_frame = ctk.CTkFrame(
            table_container,
            fg_color="#F8F9FA",
            height=50
        )
        self.pagination_frame.grid(row=1, column=0, sticky="ew")
        self.pagination_frame.grid_propagate(False)  # Force fixed height
        
        # Create pagination controls
        self.create_pagination_controls()
        
        # Load initial data
        self.load_inventory()
    
    def create_pagination_controls(self):
        """Create pagination controls in the footer"""
        # Clear existing controls
        for widget in self.pagination_frame.winfo_children():
            widget.destroy()
            
        # Create left container for "Showing" dropdown
        left_container = ctk.CTkFrame(
            self.pagination_frame,
            fg_color="transparent"
        )
        left_container.pack(side="left", padx=20, pady=10)
        
        # Add "Showing" label
        showing_label = ctk.CTkLabel(
            left_container,
            text="Showing",
            font=("", 13),
            text_color="#6F6E77"
        )
        showing_label.pack(side="left", padx=(0, 10))
        
        # Add rows per page dropdown
        self.rows_per_page_var = ctk.StringVar(value=str(self.items_per_page))
        rows_dropdown = ctk.CTkOptionMenu(
            left_container,
            values=["10", "15", "20"],
            variable=self.rows_per_page_var,
            width=70,
            height=30,
            command=self.on_rows_per_page_change,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA",
            dropdown_fg_color="white",
            dropdown_hover_color="#F8F9FA",
            dropdown_text_color="#16151C"
        )
        rows_dropdown.pack(side="left")
        
        # Create right container for page navigation
        right_container = ctk.CTkFrame(
            self.pagination_frame,
            fg_color="transparent"
        )
        right_container.pack(side="right", padx=20, pady=10)
        
        # Previous page button
        self.prev_button = ctk.CTkButton(
            right_container,
            text="",
            image=self.chevron_left_image,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=30,
            height=30,
            corner_radius=15,
            command=self.previous_page
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Create page buttons container
        pages_container = ctk.CTkFrame(
            right_container,
            fg_color="transparent"
        )
        pages_container.pack(side="left", padx=10)
        
        # Calculate total pages and visible page numbers
        total_pages = math.ceil(self.total_items / self.items_per_page)
        visible_pages = self.get_visible_page_numbers(self.current_page, total_pages)
        
        # Add page buttons
        for page_num in visible_pages:
            if page_num == "...":
                # Ellipsis
                label = ctk.CTkLabel(
                    pages_container,
                    text="...",
                    font=("", 13),
                    text_color="#6F6E77",
                    width=30
                )
                label.pack(side="left", padx=2)
            else:
                # Page button
                is_current = page_num == self.current_page
                button = ctk.CTkButton(
                    pages_container,
                    text=str(page_num),
                    fg_color="#006EC4" if is_current else "transparent",
                    text_color="white" if is_current else "#16151C",
                    hover_color="#0059A1" if is_current else "#E8E9EA",
                    width=30,
                    height=30,
                    corner_radius=15,
                    command=lambda p=page_num: self.go_to_page(p)
                )
                button.pack(side="left", padx=2)
        
        # Next page button
        self.next_button = ctk.CTkButton(
            right_container,
            text="",
            image=self.chevron_right_image,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=30,
            height=30,
            corner_radius=15,
            command=self.next_page
        )
        self.next_button.pack(side="left", padx=5)
        
        # Update button states
        self.update_pagination_buttons()
    
    def get_visible_page_numbers(self, current_page, total_pages):
        """Calculate which page numbers should be visible"""
        if total_pages <= 7:
            return list(range(1, total_pages + 1))
            
        if current_page <= 4:
            return [1, 2, 3, 4, 5, "...", total_pages]
            
        if current_page >= total_pages - 3:
            return [1, "...", total_pages-4, total_pages-3, total_pages-2, total_pages-1, total_pages]
            
        return [1, "...", current_page-1, current_page, current_page+1, "...", total_pages]
    
    def go_to_page(self, page):
        """Go to specific page number"""
        if isinstance(page, int) and page != self.current_page:
            self.current_page = page
            self.load_inventory()
    
    def on_rows_per_page_change(self, value):
        """Handle change in number of rows per page"""
        self.items_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self.load_inventory()
    
    def update_pagination_buttons(self):
        """Update the state of pagination buttons"""
        total_pages = math.ceil(self.total_items / self.items_per_page)
        
        # Update prev button
        if self.current_page <= 1:
            self.prev_button.configure(state="disabled", fg_color="#F0F0F0")
        else:
            self.prev_button.configure(state="normal", fg_color="transparent")
            
        # Update next button
        if self.current_page >= total_pages:
            self.next_button.configure(state="disabled", fg_color="#F0F0F0")
        else:
            self.next_button.configure(state="normal", fg_color="transparent")
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_inventory()
    
    def next_page(self):
        """Go to next page"""
        total_pages = math.ceil(self.total_items / self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_inventory()
    
    def on_search(self, event=None):
        """Handle search when Enter is pressed"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_inventory()
    
    def load_inventory(self):
        # Clear existing content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        try:
            # Get inventory items and apply search filter
            all_inventory = self.controller.get_all_inventory()
            
            # Filter inventory if search query exists
            if self.search_query:
                all_inventory = [
                    item for item in all_inventory 
                    if self.search_query.lower() in item["product_name"].lower() or 
                       (item["category_name"] and self.search_query.lower() in item["category_name"].lower()) or
                       (item["supplier_name"] and self.search_query.lower() in item["supplier_name"].lower())
                ]
            
            self.total_items = len(all_inventory)
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            inventory = all_inventory[start_idx:end_idx]

            if not inventory:
                no_data_text = "No inventory items found"
                if self.search_query:
                    no_data_text = f'No inventory items found for "{self.search_query}"'
                    
                no_data_label = ctk.CTkLabel(
                    self.main_content,
                    text=no_data_text,
                    font=("", 13),
                    text_color="#6F6E77"
                )
                no_data_label.grid(row=0, column=0, columnspan=4, pady=20)
            else:
                product_name_width = 200
                quantity_width = 100
                category_width = 150
                supplier_width = 150
                
                for idx, item in enumerate(inventory):
                    row_frame = ctk.CTkFrame(
                        self.main_content,
                        fg_color="transparent",
                        height=50
                    )
                    row_frame.grid(row=idx*2, column=0, columnspan=4, sticky="nsew", padx=1)
                    
                    # Configure row columns with same weights and minimum sizes
                    row_frame.grid_columnconfigure(0, weight=3, minsize=product_name_width)  # Product Name
                    row_frame.grid_columnconfigure(1, weight=2, minsize=quantity_width)  # Quantity
                    row_frame.grid_columnconfigure(2, weight=3, minsize=category_width)  # Category
                    row_frame.grid_columnconfigure(3, weight=3, minsize=supplier_width)  # Supplier

                    # Product Name with fixed width
                    product_name_label = ctk.CTkLabel(
                        row_frame,
                        text=item["product_name"],
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=product_name_width,
                        wraplength=product_name_width-30
                    )
                    product_name_label.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

                    # Quantity with fixed width
                    quantity_label = ctk.CTkLabel(
                        row_frame,
                        text=str(item["quantity"]),
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=quantity_width
                    )
                    quantity_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")

                    # Category with fixed width
                    category_label = ctk.CTkLabel(
                        row_frame,
                        text=item["category_name"] or "-",
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=category_width
                    )
                    category_label.grid(row=0, column=2, padx=10, pady=15, sticky="w")

                    # Supplier with fixed width
                    supplier_label = ctk.CTkLabel(
                        row_frame,
                        text=item["supplier_name"] or "-",
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=supplier_width
                    )
                    supplier_label.grid(row=0, column=3, padx=10, pady=15, sticky="w")

                    # Add separator
                    if idx < len(inventory) - 1:
                        separator = ctk.CTkFrame(
                            self.main_content,
                            fg_color="#F0F0F0",
                            height=1
                        )
                        separator.grid(row=idx*2+1, column=0, columnspan=4, sticky="ew", padx=20)
            
            # Update pagination controls
            self.create_pagination_controls()
            
        except Exception as e:
            print(f"Error loading inventory: {e}")
            error_label = ctk.CTkLabel(
                self.main_content,
                text=f"Error loading inventory: {str(e)}",
                font=("", 13),
                text_color="#FF4842"
            )
            error_label.pack(pady=20)
    
    def show_add_dialog(self):
        """Show dialog to add a new inventory item"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Inventory Item")
        dialog.geometry("400x300")
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product selection
        product_label = ctk.CTkLabel(content_frame, text="Product", font=("", 14, "bold"))
        product_label.pack(anchor="w", pady=(0, 10))
        
        # Assuming you have a method to get product names
        product_names = self.controller.get_product_names()
        self.selected_product = tk.StringVar(value=product_names[0] if product_names else "")
        product_dropdown = ctk.CTkOptionMenu(
            content_frame,
            values=product_names,
            variable=self.selected_product,
            width=200
        )
        product_dropdown.pack(anchor="w", pady=(0, 20))
        
        # Quantity entry
        quantity_label = ctk.CTkLabel(content_frame, text="Quantity", font=("", 14, "bold"))
        quantity_label.pack(anchor="w", pady=(0, 10))
        
        self.quantity_entry = ctk.CTkEntry(content_frame, width=200)
        self.quantity_entry.pack(anchor="w", pady=(0, 20))
        
        # Buttons
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
        
        # Add button
        add_button = ctk.CTkButton(
            buttons_frame,
            text="Add",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.add_inventory_item(dialog)
        )
        add_button.pack(side="left")
    
    def add_inventory_item(self, dialog):
        """Add inventory item logic"""
        product_name = self.selected_product.get()
        quantity = self.quantity_entry.get()
        
        if not quantity.isdigit():
            print("Invalid quantity")
            return
        
        # Assuming you have a method to get product ID by name
        product_id = self.controller.get_product_id_by_name(product_name)
        self.controller.add_inventory(product_id, int(quantity))
        dialog.destroy()
        self.load_inventory()
    
    def show_filter_dialog(self):
        """Show filter options dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Filter Inventory")
        dialog.geometry("400x300")
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product name filter
        product_name_label = ctk.CTkLabel(content_frame, text="Product Name", font=("", 14, "bold"))
        product_name_label.pack(anchor="w", pady=(0, 10))
        
        self.product_name_filter = ctk.CTkEntry(content_frame, width=200)
        self.product_name_filter.pack(anchor="w", pady=(0, 20))
        
        # Category filter
        category_label = ctk.CTkLabel(content_frame, text="Category", font=("", 14, "bold"))
        category_label.pack(anchor="w", pady=(0, 10))
        
        # Assuming you have a method to get category names
        category_names = self.controller.get_category_names()
        self.selected_category = tk.StringVar(value=category_names[0] if category_names else "")
        category_dropdown = ctk.CTkOptionMenu(
            content_frame,
            values=category_names,
            variable=self.selected_category,
            width=200
        )
        category_dropdown.pack(anchor="w", pady=(0, 20))
        
        # Buttons
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
        product_name_filter = self.product_name_filter.get().strip()
        category_filter = self.selected_category.get()
        
        # Implement filtering logic here
        # For example, you might filter the inventory list based on these criteria
        
        dialog.destroy()
        self.load_inventory()