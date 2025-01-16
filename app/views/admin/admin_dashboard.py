import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from PIL import Image
from app.views.admin.products_page import ProductsPage
from app.views.admin.categories_page import CategoriesPage
from app.views.admin.inventory_page import InventoryPage
from app.views.admin.supplier_page import SupplierPage
from app.views.admin.users_page import UsersPage
from app.views.admin.orders_page import OrdersPage

class AdminDashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data  # Store user_data for access by child components

        # Set appearance mode to light
        ctk.set_appearance_mode("light")

        print("User data:", self.user_data)
        
        self.title('Admin Dashboard')
        self.geometry('1200x700')
        self.configure(fg_color="white")  # Set main window background to white
        
        # Configure grid weights for responsive layout
        self.grid_columnconfigure(1, weight=1)  # Content area takes remaining space
        self.grid_rowconfigure(0, weight=1)     # Make the row expandable
        
        # Create main container
        main_container = ctk.CTkFrame(self, fg_color="white")
        main_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Sidebar (left half) with specific color
        sidebar = ctk.CTkFrame(main_container, fg_color="#E8FAFF", corner_radius=20)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 30))
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Set sidebar width to be approximately half the screen
        sidebar.grid_propagate(False)
        sidebar.configure(width=280)

        # Store buttons and icons for state management
        self.buttons = []
        self.icons = {}
        self.active_icons = {}

        # Define icons for each item
        icon_files = {
            'Products': 'products.png',
            'Category': 'category.png',
            'Inventory': 'inventory.png',
            'Supplier': 'supplier.png',
            'Orders': 'order.png',
            'Users': 'users.png',
            'Logout': 'logout.png'
        }

        # Load icons
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        
        # Create a frame for sidebar items with padding
        sidebar_content = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add project logo and name
        logo_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 30))
        
        # Load and display logo
        logo_path = str(Path(__file__).parent.parent.parent / 'assets' / 'logo.png')
        logo_image = Image.open(logo_path)
        logo = ctk.CTkImage(
            light_image=logo_image,
            size=(32, 32)
        )
        
        logo_label = ctk.CTkLabel(
            logo_frame, 
            image=logo, 
            text="",
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        # Add project name
        project_name = ctk.CTkLabel(
            logo_frame,
            text="Warehouse",
            font=("", 20, "bold"),
            text_color="#16151C"
        )
        project_name.pack(side="left")
        
        # Create menu container
        menu_container = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        menu_container.pack(fill="both", expand=True)
        
        # Sidebar items
        sidebar_items = ['Products', 'Category', 'Inventory', 'Supplier', 'Orders', 'Users']
        for item in sidebar_items:
            # Load and create both normal and active state icons
            icon_path = str(assets_path / icon_files[item])
            icon_image = Image.open(icon_path)
            
            # Convert to dark gray for active state
            active_image = icon_image.copy()
            active_image = active_image.convert('RGBA')
            data = active_image.getdata()
            new_data = []
            for item_data in data:
                # Change all non-transparent pixels to dark gray (#111827)
                if item_data[3] != 0:  # If pixel is not transparent
                    new_data.append((17, 24, 39, item_data[3]))  # #111827 RGB values
                else:
                    new_data.append(item_data)  # Keep transparent pixels as is
            active_image.putdata(new_data)

            # Create both normal and active icons
            normal_icon = ctk.CTkImage(
                light_image=icon_image,
                size=(24, 24)
            )
            active_icon = ctk.CTkImage(
                light_image=active_image,
                size=(24, 24)
            )
            
            # Store both versions of the icon
            self.icons[item] = normal_icon
            self.active_icons[item] = active_icon
            
            button = ctk.CTkButton(
                menu_container, 
                text=item,
                command=lambda i=item: self.show_page(i),
                fg_color="transparent",
                text_color="#16151C",
                image=normal_icon,
                compound="left",
                anchor="w",
                height=40,
                corner_radius=8,
                font=("", 13)  # Default font weight
            )
            button.pack(fill='x', pady=5)
            self.buttons.append(button)

        # Add logout button at the bottom
        logout_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent", height=50)
        logout_frame.pack(fill="x", side="bottom")
        
        # Load and create logout icon with red color
        logout_icon_path = str(assets_path / 'logout.png')
        logout_icon_image = Image.open(logout_icon_path)
        
        # Convert icon to red color
        red_icon = logout_icon_image.copy()
        red_icon = red_icon.convert('RGBA')
        data = red_icon.getdata()
        new_data = []
        for item in data:
            # Change all non-transparent pixels to red (#FF4842)
            if item[3] != 0:  # If pixel is not transparent
                new_data.append((255, 72, 66, item[3]))  # #FF4842 RGB values
            else:
                new_data.append(item)  # Keep transparent pixels as is
        red_icon.putdata(new_data)
        
        logout_icon = ctk.CTkImage(
            light_image=red_icon,
            size=(24, 24)
        )
        
        logout_button = ctk.CTkButton(
            logout_frame,
            text="Đăng xuất",
            command=self.logout,
            fg_color="transparent",
            text_color="#FF4842",  # Red color for logout
            image=logout_icon,
            compound="left",
            anchor="w",
            height=40,
            corner_radius=8,
            font=("", 13),
            hover=True,
            hover_color="#FFE8E7"  # Light red on hover
        )
        logout_button.pack(fill="x")

        # Right container for header and content
        right_container = ctk.CTkFrame(main_container, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew")
        right_container.grid_rowconfigure(1, weight=1)
        right_container.grid_columnconfigure(0, weight=1)

        # Header in right container
        header = ctk.CTkFrame(right_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        header.grid_columnconfigure(1, weight=1)  # Make middle space expand
        
        # Left side - Active page title
        self.page_title = ctk.CTkLabel(
            header,
            text="Products",  # Default page
            font=("", 24, "bold"),
            text_color="#16151C"
        )
        self.page_title.grid(row=0, column=0, sticky="w")
        
        # Right side - User info
        user_info_frame = ctk.CTkFrame(
            header,
            fg_color="transparent",
            border_color="#F0F0F0",
            border_width=2,
            corner_radius=8
        )
        user_info_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Create inner frame for username and role
        user_details_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        user_details_frame.pack(side="left", padx=10, pady=2)
        
        # Username
        username_label = ctk.CTkLabel(
            user_details_frame,
            text=user_data["ten_dang_nhap"],
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        username_label.pack(anchor="w")
        
        # Role
        role_label = ctk.CTkLabel(
            user_details_frame,
            text=user_data["ho_ten"],
            font=("", 12),
            text_color="#6F6E77"
        )
        role_label.pack(anchor="w")
        
        # Load and add chevron-down icon
        chevron_path = str(assets_path / 'chevron-down.png')
        chevron_image = Image.open(chevron_path)
        chevron_icon = ctk.CTkImage(
            light_image=chevron_image,
            size=(16, 16)
        )
        
        # Add chevron icon
        chevron_label = ctk.CTkLabel(
            user_info_frame,
            text="",
            image=chevron_icon
        )
        chevron_label.pack(side="right", padx=10, pady=8)
        
        # Content area in right container
        self.content_area = ctk.CTkFrame(right_container, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Bind resize event
        self.bind("<Configure>", self.on_resize)

        self.show_page('Products')

    def logout(self):
        """Log out the user and return to the login screen."""
        from tkinter import messagebox

        # Show confirmation dialog
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.destroy()  # Close the current dashboard window

            # Import and open the login screen
            from app.views.login_view import LoginView
            root = tk.Tk()
            login_screen = LoginView(root)
            root.mainloop()

    def on_resize(self, event):
        self.update_idletasks()

    def apply_opacity(self, hex_color, opacity):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'#{int(rgb[0])}{int(rgb[1])}{int(rgb[2])}{int(opacity * 255):02x}'

    def show_page(self, page_name):
        # Reset all buttons to default state
        for button in self.buttons:
            button_text = button.cget("text")
            button.configure(
                fg_color="transparent",
                text_color="#16151C",
                image=self.icons[button_text],
                font=("", 13)  # Reset to default weight
            )
            
        # Set active button state
        active_button = next(btn for btn in self.buttons if btn.cget("text") == page_name)
        active_button.configure(
            fg_color="#C9F1FF",
            text_color="#006EC4",
            image=self.active_icons[page_name],
            font=("", 13, "bold")
        )
        
        # Update page title
        self.page_title.configure(text=page_name)

        # Update content
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        # Create and show the appropriate page
        if page_name == "Products":
            page = ProductsPage(self.content_area, self)
        elif page_name == "Category":  
            page = CategoriesPage(self.content_area, self)
        elif page_name == "Inventory":
            page = InventoryPage(self.content_area, self)
        elif page_name == "Supplier":
            page = SupplierPage(self.content_area, self)
        elif page_name == "Users":
            page = UsersPage(self.content_area, self)
        elif page_name == "Orders":
            page = OrdersPage(self.content_area, self, self.user_data)
        else:
            page = ctk.CTkLabel(self.content_area, text=f'{page_name} Page (Content coming soon...)')
        
        page.pack(expand=True, fill="both")

if __name__ == '__main__':
    test_user_data = {"username": "Mathias"}
    app = AdminDashboard(user_data=test_user_data)
    app.mainloop()