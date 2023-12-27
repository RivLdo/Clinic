import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Testfordb import OnlineShopMedis
import pymysql

class OnlineShopGUI(tk.Tk):
    def _init_(self, connection):
        super()._init_()

        self.title("Toko Online Medis")

        self.online_shop = OnlineShopMedis(connection)

        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = tk.Frame(
            self, width=200, height=300, relief="ridge", padx=20, pady=10, bg="lightblue")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.menu_label = ttk.Label(
            self.menu_frame, text="Menu", font=("Arial", 20))
        self.menu_label.pack(pady=30)

        self.shop_btn = ttk.Button(
            self.menu_frame, text="Toko Online Medis", command=self.open_shop)
        self.shop_btn.pack(pady=10)

        self.exit_btn = ttk.Button(
            self.menu_frame, text="Keluar", command=self.destroy)
        self.exit_btn.pack(pady=10)

    def open_shop(self):
        shop_window = tk.Toplevel(self)
        shop_window.title("Toko Online Medis")
        ShopWindow(shop_window, self.online_shop)

class ShopWindow(tk.Frame):
    def _init_(self, master, online_shop):
        super()._init_(master)
        self.master = master
        self.online_shop = online_shop
        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("500x400")

        self.label = tk.Label(
            self.master, text="Selamat datang di Toko Online Medis", font=("Arial", 16))
        self.label.pack(pady=10)

        self.product_listbox = tk.Listbox(
            self.master, selectmode=tk.SINGLE, font=("Arial", 12))
        for product in self.online_shop.products:
            self.product_listbox.insert(
                tk.END, product.display_info())
        self.product_listbox.pack(pady=10)

        self.quantity_label = tk.Label(
            self.master, text="Jumlah yang akan dibeli:", font=("Arial", 12))
        self.quantity_label.pack()

        self.quantity_entry = tk.Entry(
            self.master, font=("Arial", 12))
        self.quantity_entry.pack(pady=10)

        self.add_to_cart_btn = tk.Button(
            self.master, text="Tambah ke Keranjang", command=self.add_to_cart, font=("Arial", 12))
        self.add_to_cart_btn.pack()

        self.cart_btn = tk.Button(
            self.master, text="Lihat Keranjang", command=self.view_cart, font=("Arial", 12))
        self.cart_btn.pack(pady=10)

        self.finish_shopping_btn = tk.Button(
            self.master, text="Selesai Belanja", command=self.finish_shopping, font=("Arial", 12))
        self.finish_shopping_btn.pack()

    def add_to_cart(self):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            product_choice = selected_index[0]
            quantity = self.quantity_entry.get()

            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror(
                    "Error", "Masukkan jumlah yang valid.")
                return

            self.online_shop.add_to_cart(product_choice, quantity)
            messagebox.showinfo(
                "Sukses", "Produk ditambahkan ke keranjang.")
        else:
            messagebox.showerror("Error", "Pilih produk terlebih dahulu.")

    def view_cart(self):
        self.online_shop.view_cart()

    def finish_shopping(self):
        self.online_shop.generate_invoice()
        messagebox.showinfo("Sukses", "Pembelian selesai.")
        self.master.destroy()

if __name__ == "__main__":
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='test2',
                                 cursorclass=pymysql.cursors.DictCursor)
    app = OnlineShopGUI(connection)
    app.geometry("500x400")
    app.mainloop()
