import tkinter as tk
from tkinter import ttk
import json

class ModernTheme:
    # Modern color palette
    COLORS = {
        'primary': '#2196F3',      # Blue
        'primary_dark': '#1976D2',
        'primary_light': '#BBDEFB',
        'accent': '#FF4081',       # Pink
        'warning': '#FFC107',      # Amber
        'error': '#F44336',        # Red
        'success': '#4CAF50',      # Green
        'text': '#212121',         # Almost black
        'text_secondary': '#757575',# Dark gray
        'background': '#FFFFFF',    # White
        'surface': '#F5F5F5',      # Light gray
        'divider': '#BDBDBD'       # Gray
    }

    # Font configurations
    FONTS = {
        'heading': ('Helvetica', 24, 'bold'),
        'subheading': ('Helvetica', 18, 'bold'),
        'body': ('Helvetica', 12),
        'button': ('Helvetica', 12, 'bold'),
        'small': ('Helvetica', 10)
    }

    @classmethod
    def setup(cls):
        """Setup the modern theme"""
        style = ttk.Style()
        
        # Configure main theme settings
        style.configure('Modern.TFrame', background=cls.COLORS['background'])
        style.configure('Surface.TFrame', background=cls.COLORS['surface'])
        
        # Configure button styles
        style.configure('Modern.TButton',
            background=cls.COLORS['primary'],
            foreground='white',
            padding=(20, 10),
            font=cls.FONTS['button']
        )
        style.map('Modern.TButton',
            background=[('active', cls.COLORS['primary_dark'])],
            foreground=[('active', 'white')]
        )

        # Accent button style
        style.configure('Accent.TButton',
            background=cls.COLORS['accent'],
            foreground='white',
            padding=(20, 10),
            font=cls.FONTS['button']
        )
        style.map('Accent.TButton',
            background=[('active', '#E91E63')],  # Darker pink
            foreground=[('active', 'white')]
        )

        # Warning button style
        style.configure('Warning.TButton',
            background=cls.COLORS['warning'],
            foreground=cls.COLORS['text'],
            padding=(20, 10),
            font=cls.FONTS['button']
        )

        # Error button style
        style.configure('Error.TButton',
            background=cls.COLORS['error'],
            foreground='white',
            padding=(20, 10),
            font=cls.FONTS['button']
        )

        # Success button style
        style.configure('Success.TButton',
            background=cls.COLORS['success'],
            foreground='white',
            padding=(20, 10),
            font=cls.FONTS['button']
        )

        # Entry style
        style.configure('Modern.TEntry',
            fieldbackground=cls.COLORS['background'],
            padding=(10, 5)
        )

        # Label styles
        style.configure('Modern.TLabel',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['body']
        )
        style.configure('Heading.TLabel',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['heading']
        )
        style.configure('Subheading.TLabel',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            font=cls.FONTS['subheading']
        )

        # Treeview style
        style.configure('Modern.Treeview',
            background=cls.COLORS['background'],
            fieldbackground=cls.COLORS['background'],
            foreground=cls.COLORS['text'],
            rowheight=30,
            font=cls.FONTS['body']
        )
        style.configure('Modern.Treeview.Heading',
            background=cls.COLORS['primary'],
            foreground='white',
            font=cls.FONTS['button']
        )
        style.map('Modern.Treeview',
            background=[('selected', cls.COLORS['primary'])],
            foreground=[('selected', 'white')]
        )

        # Notebook style
        style.configure('Modern.TNotebook',
            background=cls.COLORS['background'],
            tabmargins=[2, 5, 2, 0]
        )
        style.configure('Modern.TNotebook.Tab',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text'],
            padding=[20, 10],
            font=cls.FONTS['button']
        )
        style.map('Modern.TNotebook.Tab',
            background=[('selected', cls.COLORS['primary'])],
            foreground=[('selected', 'white')]
        )

        # Progressbar style
        style.configure('Modern.Horizontal.TProgressbar',
            background=cls.COLORS['primary'],
            troughcolor=cls.COLORS['surface'],
            thickness=10
        )

        # Separator style
        style.configure('Modern.TSeparator',
            background=cls.COLORS['divider']
        )

    @classmethod
    def apply_to_widget(cls, widget):
        """Apply theme to a specific widget and its children"""
        if isinstance(widget, ttk.Frame):
            widget.configure(style='Modern.TFrame')
        elif isinstance(widget, ttk.Button):
            widget.configure(style='Modern.TButton')
        elif isinstance(widget, ttk.Entry):
            widget.configure(style='Modern.TEntry')
        elif isinstance(widget, ttk.Label):
            widget.configure(style='Modern.TLabel')
        elif isinstance(widget, ttk.Treeview):
            widget.configure(style='Modern.Treeview')
        elif isinstance(widget, ttk.Notebook):
            widget.configure(style='Modern.TNotebook')
        
        # Apply to children
        for child in widget.winfo_children():
            cls.apply_to_widget(child)
