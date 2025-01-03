import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from app.views.base_view import BaseView
from app.views.dialogs.inventory_dialog import InventoryDialog

class InventoryView(BaseView):
    def __init__(self, parent=None):
        self.controller = None
        super().__init__(parent)

    def set_controller(self, controller):
        self.controller = controller

    def _setup_ui(self):
        """Setup the inventory management interface"""
        super()._setup_ui()

        # Configure main container
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header frame
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(header_frame, text="Inventory", font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, sticky="w")

        # Add button
        add_btn = ttk.Button(header_frame, text="Add Inventory", command=self._on_add_click)
        add_btn.grid(row=0, column=1, sticky="e")

        # Table frame
        table_frame = ttk.Frame(self.main_container)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Create treeview
        columns = ("ID", "Product", "Quantity", "Location", "Status", "Actions")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Actions", text="Actions")

        self.tree.column("ID", width=50)
        self.tree.column("Product", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Location", width=150)
        self.tree.column("Status", width=100)
        self.tree.column("Actions", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid the treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind double click event
        self.tree.bind("<Double-1>", self._on_row_double_click)

        # Load initial data
        self.refresh_view()

    def refresh_view(self):
        """Refresh the inventory list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load inventory
        inventory_items = self.controller.get_all()

        # Add inventory items to treeview
        for item in inventory_items:
            values = (
                item.get('id', ''),
                item.get('product_name', ''),
                item.get('quantity', ''),
                item.get('location', ''),
                item.get('status', ''),
                'Edit/Delete'
            )
            self.tree.insert('', 'end', values=values)

    def _on_add_click(self):
        """Handle add button click"""
        dialog = InventoryDialog(self)
        dialog.wait_window()  # Wait for dialog to close

        if dialog.result:
            success = self.controller.add(dialog.result)
            if success:
                self.show_info("Success", "Inventory added successfully")
                self.refresh_view()
            else:
                self.show_error("Error", "Failed to add inventory")

    def _on_row_double_click(self, event):
        """Handle row double click"""
        # Get selected item
        selection = self.tree.selection()
        if not selection:
            return

        # Get item data
        item = self.tree.item(selection[0])
        inventory_id = item['values'][0]

        # Get inventory data
        inventory = self.controller.get_by_id(inventory_id)
        if not inventory:
            self.show_error("Error", "Inventory not found")
            return

        # Show edit dialog
        dialog = InventoryDialog(self, inventory)
        dialog.wait_window()

        if dialog.result:
            success = self.controller.update(inventory_id, dialog.result)
            if success:
                self.show_info("Success", "Inventory updated successfully")
                self.refresh_view()
            else:
                self.show_error("Error", "Failed to update inventory")