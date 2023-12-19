import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    # 
)

class BillingSystem:
    def __init__(self, db_connection):
        self._db = db_connection
        self._cursor = self._db.cursor()

    def create_invoice(self):
        print("Pembuatan Faktur :")
        customer_name = input("Masukkan nama pelanggan: ")
        
        while True:
            try:
                invoice_date_str = input("Masukkan tanggal faktur (YYYY-MM-DD): ")
                invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
                break
            except ValueError:
                print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
        
        # Mencari nomor faktur yang tersedia terendah
        sql = "SELECT MIN(invoice_number) FROM invoices WHERE invoice_number NOT IN (SELECT invoice_number FROM invoices)"
        self._cursor.execute(sql)
        min_available_invoice_number = self._cursor.fetchone()[0]
        
        if min_available_invoice_number is not None:
            invoice_number = min_available_invoice_number
        else:
            # Jika tidak ada nomor faktur yang tersedia, gunakan nomor faktur tertinggi saat ini + 1
            sql = "SELECT MAX(invoice_number) FROM invoices"
            self._cursor.execute(sql)
            max_invoice_number = self._cursor.fetchone()[0]
            if max_invoice_number is None:
                invoice_number = 1
            else:
                invoice_number = max_invoice_number + 1

        total_amount = float(input("Masukkan total jumlah (Rp): "))
        
        # Menggunakan nomor faktur yang telah dihitung
        sql = "INSERT INTO invoices (invoice_number, customer_name, invoice_date, total_amount) VALUES (%s, %s, %s, %s)"
        values = (invoice_number, customer_name, invoice_date, total_amount)
        
        self._cursor.execute(sql, values)
        self._db.commit()
        
        print(f"Faktur dengan Nomor {invoice_number} sukses dibuat.\n")

    def edit_invoice(self):
        print("Mengedit Faktur")
        invoice_number = int(input("Masukkan Nomor faktur untuk diedit: "))
        
        while True:
            try:
                new_total_amount = float(input("Masukkan total jumlah baru (Rp): "))
                break
            except ValueError:
                print("Total jumlah tidak valid. Harap masukkan angka.")
        
        # Perbarui total jumlah faktur dengan nomor faktur yang sesuai
        sql = "UPDATE invoices SET total_amount = %s WHERE invoice_number = %s"
        values = (new_total_amount, invoice_number)
        
        self._cursor.execute(sql, values)
        self._db.commit()
        
        print(f"Faktur dengan Nomor {invoice_number} berhasil diubah.\n")

    def delete_invoice(self):
        print("Menghapus Faktur")
        invoice_number = int(input("Masukkan Nomor faktur untuk dihapus: "))
        
        # Hapus faktur dengan Nomor yang sesuai
        sql = "DELETE FROM invoices WHERE invoice_number = %s"
        values = (invoice_number,)
        
        self._cursor.execute(sql, values)
        self._db.commit()
        
        print(f"Faktur dengan Nomor {invoice_number} berhasil dihapus.\n")

        # Membebaskan nomor faktur untuk pengisian ulang
        sql = "UPDATE invoices SET invoice_number = NULL WHERE invoice_number = %s"
        self._cursor.execute(sql, values)
        self._db.commit()

    def view_invoices(self):
        print("{:<4} {:<20} {:<15} {:<15} {:<10}".format("No", "Customer Name", "Invoice Date", "Total Amount (Rp)", "Status"))
        print("=" * 70)
        
        sql = "SELECT invoice_number, customer_name, invoice_date, total_amount, 'Paid' AS status FROM invoices"
        self._cursor.execute(sql)
        invoices = self._cursor.fetchall()
        for invoice in invoices:
            invoice_number, customer_name, invoice_date, total_amount, status = invoice
            formatted_date = str(invoice_date)
            print("{:<4} {:<20} {:<15} {:<15} {:<10}".format(invoice_number, customer_name, formatted_date, total_amount, status))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def view_shop(self):
        print("{:<4} {:<20} {:<15} {:<15} {:<10}".format("No", "Customer Name", "Invoice Date", "Total Amount (Rp)", "Status"))
        print("=" * 70)

        sql = "SELECT order_id, customer_id, username, date, total_amount AS status FROM orders"
        self._cursor.execute(sql)
        shop = self._cursor.fetchall()
        for shoping in shop:
            order_id, customer_id, username, date, total_amount = shoping
            print("{:<4} {:<20} {:<15} {:<15} {:<10}".format(order_id, customer_id, username, date, total_amount))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def close_connection(self):
        self._cursor.close()
        self._db.close()
        print("Terima kasih. Sampai jumpa!")

if __name__ == '__main__':
    billing_system = BillingSystem(db)

    while True:
        print("Menu:")
        print("1. Pembuatan Faktur")
        print("2. Mengedit Faktur")
        print("3. Menghapus Faktur")
        print("4. Lihat Faktur")
        print("5. Keluar")
        choice = input("Pilih tindakan (1/2/3/4/5/6): ")

        if choice == '1':
            billing_system.create_invoice()
        elif choice == '2':
            billing_system.edit_invoice()
        elif choice == '3':
            billing_system.delete_invoice()
        elif choice == '4':
            billing_system.view_invoices()
        elif choice == '5':
            billing_system.close_connection()
        elif choice == '6':
            billing_system.view_shop()
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, 3, 4, atau 5.")
