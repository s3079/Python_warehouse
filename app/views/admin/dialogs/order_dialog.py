import customtkinter as ctk

class OrderDialog(ctk.CTkToplevel):
    def __init__(self, parent, order):
        super().__init__(parent)
        self.title("Chi tiết đơn hàng")
        self.geometry("400x400")
        self.order = order
        self.tao_giao_dien()

    def tao_giao_dien(self):
        order_id_label = ctk.CTkLabel(self, text=f"Mã đơn hàng: {self.order['order_id']}")
        order_id_label.pack(pady=10)

        order_date_label = ctk.CTkLabel(self, text=f"Ngày đặt: {self.order['order_date']}")
        order_date_label.pack(pady=10)

        total_amount_label = ctk.CTkLabel(self, text=f"Tổng tiền: ${self.order['total_amount']:.2f}")
        total_amount_label.pack(pady=10)

        buyer_name_label = ctk.CTkLabel(self, text=f"Người mua: {self.order['buyer_name']}")
        buyer_name_label.pack(pady=10)

        product_name_label = ctk.CTkLabel(self, text=f"Sản phẩm: {self.order['product_name']}")
        product_name_label.pack(pady=10)

        close_button = ctk.CTkButton(self, text="Đóng", command=self.destroy)
        close_button.pack(pady=20)

    def hien_thi(self):
        self.grab_set()
        self.wait_window(self)