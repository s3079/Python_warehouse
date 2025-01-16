import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from PIL import Image
from app.views.admin.products_page import ProductsPage
from app.views.admin.categories_page import CategoriesPage
from app.views.admin.inventory_page import InventoryPage
from app.views.admin.supplier_page import SupplierPage
from app.views.admin.orders_page import OrdersPage

class ManagerDashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.user_data = user_data
        self.title('Manager Dashboard')
        self.geometry('1200x700')
        self.configure(fg_color="white")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="white")
        main_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(main_container, fg_color="#E8FAFF", corner_radius=20)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 30))
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_propagate(False)
        sidebar.configure(width=280)

        # Icons
        self.buttons = []
        self.icons = {}
        self.active_icons = {}
        icon_files = {
            'Products': 'products.png',
            'Category': 'category.png',
            'Inventory': 'inventory.png',
            'Supplier': 'supplier.png',
            'Orders': 'order.png',
            'Logout': 'logout.png'
        }
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        
        # Sidebar content
        sidebar_content = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo
        logo_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 30))
        logo_path = str(Path(__file__).parent.parent.parent / 'assets' / 'logo.png')
        logo_image = Image.open(logo_path)
        logo = ctk.CTkImage(light_image=logo_image, size=(32, 32))
        logo_label = ctk.CTkLabel(logo_frame, image=logo, text="")
        logo_label.pack(side="left", padx=(0, 10))
        project_name = ctk.CTkLabel(logo_frame, text="Warehouse", font=("", 20, "bold"), text_color="#16151C")
        project_name.pack(side="left")
        
        # Menu
        menu_container = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        menu_container.pack(fill="both", expand=True)
        sidebar_items = ['Products', 'Category', 'Inventory', 'Supplier', 'Orders']
        for item in sidebar_items:
            icon_path = str(assets_path / icon_files[item])
            icon_image = Image.open(icon_path)
            active_image = icon_image.copy().convert('RGBA')
            data = active_image.getdata()
            new_data = [(17, 24, 39, item_data[3]) if item_data[3] != 0 else item_data for item_data in data]
            active_image.putdata(new_data)
            normal_icon = ctk.CTkImage(light_image=icon_image, size=(24, 24))
            active_icon = ctk.CTkImage(light_image=active_image, size=(24, 24))
            self.icons[item] = normal_icon
            self.active_icons[item] = active_icon
            button = ctk.CTkButton(menu_container, text=item, command=lambda i=item: self.show_page(i),
                                   fg_color="transparent", text_color="#16151C", image=normal_icon,
                                   compound="left", anchor="w", height=40, corner_radius=8, font=("", 13))
            button.pack(fill='x', pady=5)
            self.buttons.append(button)

        # Logout button
        logout_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent", height=50)
        logout_frame.pack(fill="x", side="bottom")
        logout_icon_path = str(assets_path / 'logout.png')
        logout_icon_image = Image.open(logout_icon_path)
        red_icon = logout_icon_image.copy().convert('RGBA')
        data = red_icon.getdata()
        new_data = [(255, 72, 66, item[3]) if item[3] != 0 else item for item in data]
        red_icon.putdata(new_data)
        logout_icon = ctk.CTkImage(light_image=red_icon, size=(24, 24))
        logout_button = ctk.CTkButton(logout_frame, text="Log Out", command=self.logout,
                                      fg_color="transparent", text_color="#FF4842", image=logout_icon,
                                      compound="left", anchor="w", height=40, corner_radius=8, font=("", 13),
                                      hover=True, hover_color="#FFE8E7")
        logout_button.pack(fill="x")

        # Right container
        right_container = ctk.CTkFrame(main_container, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew")
        right_container.grid_rowconfigure(1, weight=1)
        right_container.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(right_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        header.grid_columnconfigure(1, weight=1)
        self.page_title = ctk.CTkLabel(header, text="Products", font=("", 24, "bold"), text_color="#16151C")
        self.page_title.grid(row=0, column=0, sticky="w")
        user_info_frame = ctk.CTkFrame(header, fg_color="transparent", border_color="#F0F0F0", border_width=2, corner_radius=8)
        user_info_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        user_details_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        user_details_frame.pack(side="left", padx=10, pady=2)
        username_label = ctk.CTkLabel(user_details_frame, text=user_data["username"], font=("", 13, "bold"), text_color="#16151C")
        username_label.pack(anchor="w")
        role_label = ctk.CTkLabel(user_details_frame, text="Manager", font=("", 12), text_color="#6F6E77")
        role_label.pack(anchor="w")
        chevron_path = str(assets_path / 'chevron-down.png')
        chevron_image = Image.open(chevron_path)
        chevron_icon = ctk.CTkImage(light_image=chevron_image, size=(16, 16))
        chevron_label = ctk.CTkLabel(user_info_frame, text="", image=chevron_icon)
        chevron_label.pack(side="right", padx=10, pady=8)

        # Content area
        self.content_area = ctk.CTkFrame(right_container, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Bind resize event
        self.bind("<Configure>", self.on_resize)

        # Activate Dashboard by default
        self.show_page('Products')

    def logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.destroy()
            from app.views.login_view import LoginView
            root = tk.Tk()
            login_screen = LoginView(root)
            root.mainloop()

    def on_resize(self, event):
        self.update_idletasks()

    def show_page(self, page_name):
        for button in self.buttons:
            button_text = button.cget("text")
            button.configure(fg_color="transparent", text_color="#16151C", image=self.icons[button_text], font=("", 13))
        active_button = next(btn for btn in self.buttons if btn.cget("text") == page_name)
        active_button.configure(fg_color="#C9F1FF", text_color="#006EC4", image=self.active_icons[page_name], font=("", 13, "bold"))
        self.page_title.configure(text=page_name)
        for widget in self.content_area.winfo_children():
            widget.destroy()
        if page_name == "Products":
            page = ProductsPage(self.content_area, self)
        elif page_name == "Category":
            page = CategoriesPage(self.content_area, self)
        elif page_name == "Inventory":
            page = InventoryPage(self.content_area, self)
        elif page_name == "Supplier":
            page = SupplierPage(self.content_area, self)
        elif page_name == "Orders":
            page = OrdersPage(self.content_area, self, self.user_data)
        else:
            page = ctk.CTkLabel(self.content_area, text=f'{page_name} Page (Content coming soon...)')
        page.pack(expand=True, fill="both")

# if __name__ == '__main__':
#     test_user_data = {"username": "Manager"}
#     app = ManagerDashboard(user_data=test_user_data)
#     app.mainloop() 