import customtkinter as ctk
from PIL import Image
from pathlib import Path
import tkinter as tk
from app.controllers.product_controller import ProductController
from app.views.admin.dialogs.product_dialog import ProductDialog
from app.views.admin.dialogs.center_dialog import CenterDialog
from app.views.admin.dialogs.delete_dialog import DeleteDialog
from app.views.admin.dialogs.filter_dialog import FilterDialog

class ProductsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = ProductController()
        self.can_edit = can_edit
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
            placeholder_text="Tìm kiếm sản phẩm...",
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
            text='Lọc',
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
            text='Thêm Sản Phẩm',
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
            {"name": "Tên sản phẩm", "key": "ten", "width": 100},
            {"name": "Mô tả", "key": "mo_ta", "width": 150},
            {"name": "Danh mục", "key": "ten_danh_muc", "width": 150},
            {"name": "Nhà cung cấp", "key": "ten_ncc", "width": 100},
            {"name": "Đơn giá", "key": "don_gia", "width": 150},
            {"name": "Thao tác", "key": "actions", "width": 100}
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
        products, total_count = self.controller.laySanPhamPhanTrang(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query,
            name_sort=getattr(self, 'name_sort_value', 'none'),
            price_sort=getattr(self, 'price_sort_value', 'none')
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
                    
                elif col["key"] == "don_gia":
                    # Format price in VND
                    value = f"{float(product[col['key']]):,.0f} ₫"
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                else:
                    # Regular text columns with truncation
                    value = str(product.get(col["key"], "") or "")
                    full_text = value  # Store full text for tooltip
                    
                    # Truncate text if too long
                    max_chars = col["width"] // 8  # Approximate characters that fit in width
                    if len(value) > max_chars:
                        value = value[:max_chars-3] + "..."
                    
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                    # Create tooltip for truncated text
                    if len(value) != len(full_text):
                        self.create_tooltip(label, full_text)
            
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
            text=f"Hiển thị {start_index}-{end_index} của {self.total_items} sản phẩm",
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
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show dialog to add a new product"""
        dialog = ProductDialog(
            self,
            on_save=self.save_product
        )

    def show_edit_dialog(self, product):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        print("product", product)
        """Show dialog to edit a product"""
        # Create product data dictionary with the required format
        product_data = {
            "ma_san_pham": product["ma_san_pham"],
            "ten": product["ten"],
            "mo_ta": product["mo_ta"],
            "don_gia": product["don_gia"],
            "ma_danh_muc": product["ma_danh_muc"],
            "ma_ncc": product["ma_ncc"]
        }
        
        dialog = ProductDialog(
            self,
            product=product_data,  # Pass existing product data
            on_save=self.save_product,
        )

    def delete_product(self, product):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show confirmation dialog and delete product"""
        def handle_delete():
            try:
                success, message = self.controller.xoaSanPham(product["ma_san_pham"])
                if success:
                    self.load_products()  # Refresh the list
                else:
                    from tkinter import messagebox
                    messagebox.showerror("Lỗi", message)
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", str(e))
        
        DeleteDialog(
            self,
            product["ten"],
            on_confirm=handle_delete
        )

    def show_filter_dialog(self):
        """Show filter options dialog"""
        dialog = CenterDialog(self, "Lọc Sản Phẩm", "400x300")
        
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
            text="Tên Sản Phẩm",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
        # Name radio buttons
        name_options_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_options_frame.pack(fill="x")
        
        name_all = ctk.CTkRadioButton(
            name_options_frame,
            text="Tất Cả",
            variable=self.name_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        name_all.pack(side="left", padx=(0, 15))
        
        name_asc = ctk.CTkRadioButton(
            name_options_frame,
            text="Từ A-Z",
            variable=self.name_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        name_asc.pack(side="left", padx=(0, 15))
        
        name_desc = ctk.CTkRadioButton(
            name_options_frame,
            text="Từ Z-A",
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
            text="Giá",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        price_label.pack(anchor="w", pady=(0, 10))
        
        # Price radio buttons
        price_options_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_options_frame.pack(fill="x")
        
        price_all = ctk.CTkRadioButton(
            price_options_frame,
            text="Tất Cả",
            variable=self.price_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        price_all.pack(side="left", padx=(0, 15))
        
        price_asc = ctk.CTkRadioButton(
            price_options_frame,
            text="Thấp đến Cao",
            variable=self.price_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        price_asc.pack(side="left", padx=(0, 15))
        
        price_desc = ctk.CTkRadioButton(
            price_options_frame,
            text="Cao đến Thấp",
            variable=self.price_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        price_desc.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Hủy",
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
            text="Áp Dụng",
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
        self.name_sort_value = self.name_sort.get()
        self.price_sort_value = self.price_sort.get()
        self.load_products()

    def save_product(self, data):
        """Save or update product"""
        try:
            # Validate price format and range
            try:
                price = float(data['don_gia'])
                if price < 0 or price > 999999999:  # Increased max value for VND
                    raise ValueError("Giá phải nằm trong khoảng từ 0 đến 999,999,999 ₫")
                price = round(price, 0)  # Round to whole numbers for VND
            except ValueError as e:
                if "phải nằm trong khoảng" in str(e):
                    raise e
                raise ValueError("Giá phải là một số hợp lệ")

            print("data---", data)

            # Map the dialog data to match the schema field names
            product_data = {
                'ten': data['ten'],
                'mo_ta': data['mo_ta'],
                'don_gia': price,
                'ma_danh_muc': data['ma_danh_muc'],
                'ma_ncc': data['ma_ncc']
            }

            if "ma_san_pham" in data:
                # Update existing product
                success = self.controller.capNhatSanPham(data["ma_san_pham"], product_data)
            else:
                # Add new product
                success = self.controller.themSanPham(product_data)
            
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

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ctk.CTkLabel(
                tooltip,
                text=text,
                fg_color="#16151C",
                text_color="white",
                corner_radius=6
            )
            label.pack(padx=10, pady=5)
            
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind("<Leave>", hide_tooltip)
            tooltip.bind("<Leave>", hide_tooltip)
            
        widget.bind("<Enter>", show_tooltip)
