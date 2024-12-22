import tkinter as tk
from tkinter import ttk
from app.views.base_view import BaseView

class CategoryView(BaseView):
    def _setup_ui(self):
        # Create main container
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tree view for categories
        self.tree = ttk.Treeview(
            self.content_frame, 
            columns=("ID", "Name", "Description"),
            show="headings"
        )
        
        # Setup columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self.frame, text="Category Details")
        self.form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form fields
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(self.form_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add buttons
        ttk.Button(self.buttons_frame, text="Add", command=self._on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Update", command=self._on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Delete", command=self._on_delete).pack(side=tk.LEFT, padx=5)
        
        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def refresh(self, categories=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        if categories:
            for category in categories:
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        category["category_id"],
                        category["name"],
                        category["description"]
                    )
                )
    
    def _on_add(self):
        if self.controller:
            self.controller.add_category(
                self.name_var.get(),
                self.desc_var.get()
            )
    
    def _on_update(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a category to update")
            return
            
        if self.controller:
            category_id = self.tree.item(selected[0])["values"][0]
            self.controller.update_category(
                category_id,
                self.name_var.get(),
                self.desc_var.get()
            )
    
    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a category to delete")
            return
            
        if self.controller:
            category_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_category(category_id)
    
    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.name_var.set(values[1])
            self.desc_var.set(values[2])
