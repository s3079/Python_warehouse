import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from app.controllers.product_controller import ProductController

class UserDashboard(ttk.Frame):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self._init_controllers()
        self._setup_ui()
        
    def _init_controllers(self):
        """Initialize controllers"""
        self._product_controller = ProductController(self)

    def _setup_ui(self):
        """Setup the user dashboard interface"""
        # Configure grid
        self.grid(sticky="nsew")
        self.grid_columnconfigure(1, weight=1)  # Content area expands
        self.grid_rowconfigure(0, weight=1)
        
        # Create and configure style
        self.style = ttk.Style()
        self.style.configure('Sidebar.TFrame', background='#EBF3FA')
        self.style.configure('Content.TFrame', background='white')
        self.style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'))
        self.style.configure('Menu.TButton', font=('Helvetica', 12), padding=10)
        
        # Create main frames
        self._create_sidebar()
        self._create_content_area()
        
    def _create_sidebar(self):
        """Create sidebar with navigation"""
        sidebar = ttk.Frame(self, style='Sidebar.TFrame', width=250)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        
        # Logo and title
        logo_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        logo_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Load and display logo if exists
        try:
            logo_img = Image.open("app/assets/logo.png")
            logo_img = logo_img.resize((32, 32), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(logo_frame, image=logo_photo, style='Sidebar.TFrame')
            logo_label.image = logo_photo  # Keep reference
            logo_label.grid(row=0, column=0, padx=(0, 10))
        except:
            pass  # Skip logo if file not found
        
        title_label = ttk.Label(logo_frame, text="Inventory", 
                              style='Header.TLabel')
        title_label.grid(row=0, column=1)
        
        # Menu items
        menu_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        menu_frame.grid(row=1, column=0, sticky="ew", padx=10)
        
        self.menu_buttons = {}
        menu_items = [
            ("Dashboard", "grid.png"),
            ("Products", "box.png"),
            ("Inventory", "package.png"),
            ("Settings", "settings.png")
        ]
        
        for i, (text, _) in enumerate(menu_items):
            btn = ttk.Button(menu_frame, text=text, style='Menu.TButton',
                           command=lambda t=text: self._handle_menu_click(t))
            btn.grid(row=i, column=0, sticky="ew", pady=2)
            self.menu_buttons[text] = btn
        
        # Theme switcher at bottom
        theme_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        theme_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=20)
        
        light_btn = ttk.Button(theme_frame, text="Light", style='Menu.TButton')
        light_btn.grid(row=0, column=0, padx=2)
        
        dark_btn = ttk.Button(theme_frame, text="Dark", style='Menu.TButton')
        dark_btn.grid(row=0, column=1, padx=2)
        
    def _create_content_area(self):
        """Create main content area"""
        self.content_frame = ttk.Frame(self, style='Content.TFrame')
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Create pages
        self.pages = {}
        self._setup_items_page()  # Initial page
        
    def _setup_items_page(self):
        """Set up the items page with view-only functionality"""
        page = ttk.Frame(self.content_frame)
        page.grid(row=0, column=0, sticky="nsew")
        page.grid_columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.Frame(page)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title area
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        page_title = ttk.Label(title_frame, text="Available Items",
                             style='Header.TLabel')
        page_title.grid(row=0, column=0, sticky="w")
        
        subtitle = ttk.Label(title_frame, text="View available items and their details")
        subtitle.grid(row=1, column=0, sticky="w")
        
        # Search and user area
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=0, column=1, sticky="e")
        
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.insert(0, "Search")
        search_entry.grid(row=0, column=0, padx=5)
        
        notif_btn = ttk.Button(search_frame, text="🔔")
        notif_btn.grid(row=0, column=1, padx=5)
        
        user_btn = ttk.Button(search_frame, text="User")
        user_btn.grid(row=0, column=2, padx=5)
        
        # Toolbar
        toolbar_frame = ttk.Frame(page)
        toolbar_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        toolbar_frame.grid_columnconfigure(1, weight=1)
        
        # Item search
        item_search = ttk.Entry(toolbar_frame, width=40)
        item_search.insert(0, "Search Item")
        item_search.grid(row=0, column=0, padx=5)
        
        # Filter button
        filter_btn = ttk.Button(toolbar_frame, text="Filter")
        filter_btn.grid(row=0, column=2, padx=5)
        
        # Table
        table_frame = ttk.Frame(page)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        columns = ("name", "model", "type", "store", "amount", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        self.table.heading("name", text="Item Name")
        self.table.heading("model", text="Model")
        self.table.heading("type", text="Type")
        self.table.heading("store", text="Store")
        self.table.heading("amount", text="Amount")
        self.table.heading("status", text="Status")
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical",
                               command=self.table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal",
                               command=self.table.xview)
        self.table.configure(yscrollcommand=y_scroll.set,
                           xscrollcommand=x_scroll.set)
        
        # Grid table and scrollbars
        self.table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Load items
        self._load_items()
        
        # Pagination
        pagination_frame = ttk.Frame(page)
        pagination_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        pagination_frame.grid_columnconfigure(1, weight=1)
        
        showing_label = ttk.Label(pagination_frame,
                                text="Showing 1 to 10 out of 40 records")
        showing_label.grid(row=0, column=0, sticky="w")
        
        page_combo = ttk.Combobox(pagination_frame, values=["10", "20", "30", "40", "50"],
                                width=10, state="readonly")
        page_combo.set("10")
        page_combo.grid(row=0, column=2, sticky="e")
        
        self.pages['Products'] = page
        
    def _load_items(self):
        """Load items into the table"""
        # Clear existing items
        for item in self.table.get_children():
            self.table.delete(item)
            
        # Load new items
        items = self._product_controller.get_all()
        for item in items:
            self.table.insert("", "end", values=(
                item['name'],
                item.get('model', ''),
                item.get('type', 'IE Project Items'),
                item.get('store', 'HQ Main Store'),
                f"{item.get('quantity', 0)} pcs",
                item.get('status', 'Available')
            ))
            
    def _handle_menu_click(self, menu_text):
        """Handle menu button clicks"""
        if menu_text in self.pages:
            for page in self.pages.values():
                page.grid_remove()
            self.pages[menu_text].grid()
        else:
            tk.messagebox.showinfo("Info", 
                                 f"The {menu_text} page is not implemented yet.")
