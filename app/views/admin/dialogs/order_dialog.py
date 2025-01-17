import customtkinter as ctk

class OrderDialog(ctk.CTkToplevel):
    def __init__(self, parent, order):
        super().__init__(parent)
        self.title("Order Details")
        self.geometry("400x400")
        self.order = order
        self.create_widgets()

    def create_widgets(self):
        order_id_label = ctk.CTkLabel(self, text=f"Order ID: {self.order['order_id']}")
        order_id_label.pack(pady=10)

        order_date_label = ctk.CTkLabel(self, text=f"Order Date: {self.order['order_date']}")
        order_date_label.pack(pady=10)

        total_amount_label = ctk.CTkLabel(self, text=f"Total Amount: ${self.order['total_amount']:.2f}")
        total_amount_label.pack(pady=10)

        buyer_name_label = ctk.CTkLabel(self, text=f"Buyer: {self.order['buyer_name']}")
        buyer_name_label.pack(pady=10)

        product_name_label = ctk.CTkLabel(self, text=f"Product: {self.order['product_name']}")
        product_name_label.pack(pady=10)

        close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        close_button.pack(pady=20)

    def show(self):
        self.grab_set()
        self.wait_window(self) 