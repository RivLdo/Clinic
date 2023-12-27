from abc import ABC, abstractmethod
import datetime
import pymysql.cursors
from prettytable import PrettyTable

class BaseProduct(ABC):
    def _init_(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def display_info(self):
        pass

class Product(BaseProduct):
    def display_info(self):
        return f"{self.name} - Rp {self.price}"

class BaseCustomer(ABC):
    def _init_(self, connection, current_customer_id):
        self.connection = connection
        self._username = None
        self.current_order_id = 0
        self.current_customer_id = current_customer_id

    @abstractmethod
    def create_account(self):
        pass

    @abstractmethod
    def login(self):
        pass

class Customer(BaseCustomer):
    def create_account(self):
        username = input("Masukkan username baru: ")
        password = input("Masukkan password baru: ")
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO customer (customer_id, username, password) VALUES (%s, %s, %s)",
                           (self.current_customer_id, username, password))
            self.connection.commit()
            print("Akun berhasil dibuat. Silakan login.")
            self.current_customer_id += 1
        except Exception as e:
            self.connection.rollback()
            print(f"Error: {e}")
        cursor.close()

    def login(self):
        while True:
            print("1. Login")
            print("2. Buat Akun Baru")
            choice = input("Pilih opsi (1/2): ")
            if choice == "1":
                username = input("Masukkan username: ")
                password = input("Masukkan password: ")
                cursor = self.connection.cursor()
                cursor.execute("SELECT customer_id, username FROM customer WHERE username = %s AND password = %s",
                               (username, password))
                customer_data = cursor.fetchone()
                cursor.close()
                if customer_data:
                    self._username = customer_data["username"]
                    print(f"Halo, {self._username}!")
                    return customer_data["customer_id"]
                else:
                    print("Login gagal. Periksa kembali username dan password.")
            elif choice == "2":
                self.create_account()
            else:
                print("Pilihan tidak valid. Silakan pilih 1 atau 2.")

class OnlineShopMedis(Customer):
    def _init_(self, connection, current_customer_id):
        super()._init_(connection, current_customer_id)
        self.products = [
            Product("Hansaplast", 5000),
            Product("Betadine", 10000),
            Product("Thrombophob", 65000),
            Product("Verband", 6000),
            Product("Redoxon", 70000),
            Product("Paramex", 5000),
            Product("Panadol", 15000),
            Product("Counterpain", 35000),
            Product("Salonpas", 35000)
        ]
        self.cart = []
        self.total_price = 0

    def start_shopping(self):
        customer_id = self.login()
        if customer_id is None:
            return

        while True:
            print("\nSelamat datang di Toko Online Medis")
            self.show_products()

            product_choice = input(
                "Pilih produk (masukkan nomor produk, q untuk keluar, h untuk hapus barang, c untuk cek keranjang): ")
            if product_choice == "q":
                break
            elif product_choice == "h":
                self.remove_from_cart_input()
                continue
            elif product_choice == "c":
                self.view_cart()
                continue

            try:
                quantity = int(product_choice)
            except ValueError:
                print("Masukan tidak valid. Silakan masukkan nomor produk, q, h, atau c.")
                continue

            quantity = int(input("Jumlah yang akan dibeli: "))
            self.add_to_cart(product_choice, quantity)

            while True:
                continue_shopping = input("Lanjut belanja (t), Hapus barang (h), atau Selesai (s)? ")
                if continue_shopping == "t":
                    break
                elif continue_shopping == "h":
                    self.view_cart()
                    self.remove_from_cart_input()
                elif continue_shopping == "s":
                    self.generate_invoice(customer_id)
                    return
                else:
                    print("Masukan tidak valid. Silakan masukkan t, h, atau s.")

    def remove_from_cart_input(self):
        if self.cart:
            cart_choice = input("Pilih produk dalam keranjang yang akan dihapus (masukkan nomor produk): ")
            self.remove_from_cart(cart_choice)
        else:
            print("Keranjang belanja kosong. Tidak ada produk untuk dihapus.")

    def show_products(self):
        print("Daftar Produk Medis:")
        for i, product in enumerate(self.products, start=1):
            print(f"{i}. {product.display_info()}")

    def add_to_cart(self, product_choice, quantity):
        product_choice = int(product_choice) - 1
        if 0 <= product_choice < len(self.products):
            product = self.products[product_choice]
            total_product_price = product.price * quantity
            self.cart.append({"nama": product.name, "jumlah": quantity, "harga": total_product_price})
            self.total_price += total_product_price
            print(f"{product.name} x{quantity} ditambahkan ke keranjang.")
            self.view_cart()
        else:
            print("Pilihan produk tidak valid.")

    def remove_from_cart(self, cart_choice):
        if not self.cart:
            print("Keranjang belanja kosong.")
            return

        cart_choice = int(cart_choice) - 1
        if 0 <= cart_choice < len(self.cart):
            product = self.cart[cart_choice]
            self.total_price -= product['harga']
            print(f"{product['nama']} x{product['jumlah']} dihapus dari keranjang.")
            del self.cart[cart_choice]
            self.view_cart()
        else:
            print("Pilihan produk dalam keranjang tidak valid.")

    def view_cart(self):
        if not self.cart:
            print("Keranjang belanja kosong.")
        else:
            print("\n== Keranjang Belanja ==")
            for i, item in enumerate(self.cart, start=1):
                print(f"{i}. {item['nama']} x{item['jumlah']} - Rp {item['harga']}")
            print(f"Total Harga: Rp {self.total_price}")
            print("============================")

    def generate_invoice(self, customer_id):
        now = datetime.datetime.now()
        tanggal1 = now.strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO orders (order_id, customer_id, username, date, total_amount) VALUES (%s, %s, %s, %s, %s)",
                (self.current_order_id, customer_id, self._username, tanggal1, self.total_price))
            self.connection.commit()
            self.current_order_id += 1
        except Exception as e:
            self.connection.rollback()
            print(f"Error: {e}")
            return

        cursor.execute("SELECT LAST_INSERT_ID()")
        order_id = cursor.fetchone()["LAST_INSERT_ID()"]

        cursor.close()
        self.print_invoice(order_id)

    def print_invoice(self, order_id):
        now = datetime.datetime.now()
        tanggal2 = now.strftime("%Y-%m-%d")
        jam = now.strftime("%H:%M")

        invoice_table = PrettyTable()
        invoice_table.field_names = ["No.", "Nama Barang", "Kuantitas", "Harga Satuan", "Jumlah Harga"]

        total_pembelian = 0

        for i, item in enumerate(self.cart, start=1):
            harga_satuan = item['harga']
            kuantitas = item['jumlah']
            jumlah_harga = kuantitas * harga_satuan
            total_pembelian += jumlah_harga

            invoice_table.add_row([i, item['nama'], kuantitas, f"Rp {harga_satuan}", f"Rp {jumlah_harga}"])

        print("\n======================= Nota Pembelian =======================")
        print(f"Nomor Pesanan : {order_id}")
        print(f"Tanggal       : {tanggal2}")
        print(f"Jam           : {jam}")
        print("--------------------------------------------------------------")
        print(invoice_table)
        print("--------------------------------------------------------------")
        print(f"Total Pembayaran: Rp {total_pembelian}")
        print("==============================================================")

if _name_ == "_main_":
    online_shop = OnlineShopMedis(
        connection=pymysql.connect(host='localhost',
                                   user='root',
                                   password='',
                                   database='test2',
                                   cursorclass=pymysql.cursors.DictCursor),
        current_customer_id=0
    )
    online_shop.start_shopping()
