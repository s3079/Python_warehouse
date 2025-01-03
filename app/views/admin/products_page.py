import customtkinter as ctk
from PIL import Image
from pathlib import Path
from app.controllers.product_controller import ProductController

class ProductsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = ProductController()  # Initialize the actual controller
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Table view will expand
        
        # Create top section container
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)  # Search frame will expand
        
        # Create search frame
        search_frame = ctk.CTkFrame(
            top_section,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        search_frame.grid(row=0, column=0, sticky="w")
        
        # Load search icon
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        search_icon_path = str(assets_path / 'search.png')
        search_icon_image = Image.open(search_icon_path)
        search_icon = ctk.CTkImage(
            light_image=search_icon_image,
            dark_image=search_icon_image,
            size=(20, 20)
        )
        
        # Add search icon
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        # Add search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search products...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add filter button
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Filter",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=45,
            corner_radius=8
        )
        filter_button.pack(side="left", padx=(0, 10))
        
        # Add new product button
        new_product_button = ctk.CTkButton(
            buttons_frame,
            text="Add Product",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=120,
            height=45,
            corner_radius=8
        )
        new_product_button.pack(side="left")
        
        # Create table view container
        table_container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", padx=20)
        
        # Configure table container grid
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)
        
        # Add table header
        header_frame = ctk.CTkFrame(table_container, fg_color="#F8F9FA", height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=1, pady=1)
        
        # Define column widths (adjust as needed)
        self.col_widths = {
            "Name": 250,
            "Description": 300,
            "Category": 150,
            "Supplier": 150,
            "Price": 100,
            "Actions": 100
        }
        
        # Create header labels
        current_x = 10
        for col, width in self.col_widths.items():
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=("", 13, "bold"),
                text_color="#16151C",
                width=width
            )
            label.place(x=current_x, y=15)
            current_x += width
        
        # Add scrollable frame for table content
        self.table_content = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent",
            corner_radius=0
        )
        self.table_content.grid(row=1, column=0, sticky="nsew")
        
        # Load initial data
        self.load_products()
    
    def load_products(self):
        # Clear existing content
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        try:
            # Get products from controller
            products = self.controller.get_all_products()
            
            if not products:
                # Show no products message
                no_data_label = ctk.CTkLabel(
                    self.table_content,
                    text="No products found",
                    font=("", 13),
                    text_color="#6F6E77"
                )
                no_data_label.pack(pady=20)
                return
            
            # Add products to table
            for i, product in enumerate(products):
                row_frame = ctk.CTkFrame(
                    self.table_content,
                    fg_color="transparent",
                    height=60
                )
                row_frame.pack(fill="x", pady=1)
                row_frame.pack_propagate(False)
                
                # Add product data
                current_x = 10
                col_data = [
                    product["name"],
                    product["description"][:50] + "..." if len(product["description"]) > 50 else product["description"],
                    product["category_name"],
                    product["supplier_name"],
                    f"${product['unit_price']:.2f}",
                    "..."  # Actions
                ]
                
                for text, width in zip(col_data, self.col_widths.values()):
                    label = ctk.CTkLabel(
                        row_frame,
                        text=text,
                        font=("", 13),
                        text_color="#16151C",
                        width=width
                    )
                    label.place(x=current_x, y=20)
                    current_x += width
                
                # Add separator
                separator = ctk.CTkFrame(
                    self.table_content,
                    fg_color="#F0F0F0",
                    height=1
                )
                separator.pack(fill="x")
        except Exception as e:
            # Show error message
            error_label = ctk.CTkLabel(
                self.table_content,
                text=f"Error loading products: {str(e)}",
                font=("", 13),
                text_color="#FF4842"
            )
            error_label.pack(pady=20)
