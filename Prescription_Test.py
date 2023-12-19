from PrescriptionBase import PrescriptionBase
import pymysql.cursors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import tkinter as tk
from tkinter import ttk


class InsertPrescription(PrescriptionBase):
    def operate(self, ID_Obat):
        cursor = self.conn.cursor()

        try:
            insert_query = "INSERT INTO `prescription_data` (`ID_Obat`) VALUES (%s)"
            cursor.execute(insert_query, ID_Obat)
            self.conn.commit()
            # self.__ID_obat[ID_Obat] = ID_Obat
            print(f"Obat dengan ID: {ID_Obat} telah ditambahkan di list dan database.")
        except pymysql.Error as err:
            print(f'Error saat INSERT: {err}')
        finally:
            cursor.close()

class DeletePrescription(PrescriptionBase):
    def operate(self, ID_Obat):
        cursor = self.conn.cursor()

        try:
            delete_query = "DELETE FROM `prescription_data` WHERE `ID_Obat` = %s"
            cursor.execute(delete_query, (ID_Obat,))
            self.conn.commit()
            print(f"Obat dengan ID: {ID_Obat} telah dihapus dari list dan database.")

        except pymysql.Error as err:
            print(f'Error saat DELETE: {err}')
        finally:
            cursor.close()
            
    def get_all_data(self):
        cursor = self.conn.cursor()

        try:
            select_query = "SELECT * FROM `prescription_data`"
            cursor.execute(select_query)
            data = cursor.fetchall()
            return data
        except pymysql.Error as err:
            print(f'Error saat SELECT: {err}')
            return []
        finally:
            cursor.close()

class UpdatePrescription(PrescriptionBase):
    def operate(self, ID_Obat, new_ID_Obat):
        cursor = self.conn.cursor()

        try:
            select_query = "SELECT * FROM `prescription_data` WHERE `ID_Obat` = %s"
            cursor.execute(select_query, (ID_Obat,))
            existing_data = cursor.fetchone()
            if existing_data:
                update_query = "UPDATE `prescription_data` SET `ID_Obat` = %s WHERE `ID_Obat` = %s"
                cursor.execute(update_query, (new_ID_Obat, ID_Obat))
                self.conn.commit()
                print(f"Obat dengan ID: {ID_Obat} telah diperbarui menjadi {new_ID_Obat} di database.")
            else:
                print(f"Obat dengan ID: {ID_Obat} tidak ditemukan dalam database, perbaruan tidak dapat dilakukan.")
        except pymysql.Error as err:
            print(f'Error saat UPDATE: {err}')
        finally:
            cursor.close()



class PrescriptionApp:
    def __init__(self, master):
        self.master = master
        # master.title("Prescription App")

        self.tab_control = ttk.Notebook(master)

        self.insert_tab = ttk.Frame(self.tab_control)
        self.delete_tab = ttk.Frame(self.tab_control)
        self.update_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.insert_tab, text='Insert')
        self.tab_control.add(self.delete_tab, text='Delete')
        self.tab_control.add(self.update_tab, text='Update')

        self.tab_control.pack(expand=1, fill='both')

        self.create_insert_tab()
        self.create_delete_tab()
        self.create_update_tab()

        self.delete_listbox = tk.Listbox(self.delete_tab)
        self.delete_listbox.grid(row=2, column=0, columnspan=2, pady=10)
        self.update_delete_listbox()

        

    def create_insert_tab(self):
        self.label_insert = tk.Label(self.insert_tab, text="ID Obat untuk ditamnbah:")
        self.label_insert.grid(row=0, column=0, padx=10, pady=10)

        self.entry_insert = tk.Entry(self.insert_tab)
        self.entry_insert.grid(row=0, column=1, padx=10, pady=10)

        self.button_insert = tk.Button(self.insert_tab, text="Insert", command=self.insert_operation)
        self.button_insert.grid(row=1, column=0, columnspan=2, pady=10)

    def update_delete_listbox(self):
        # Fungsi untuk mengupdate listbox dengan data dari database
        delete_operation = DeletePrescription("Clinic A")
        data = delete_operation.get_all_data()
        delete_operation.close_connection()

        self.delete_listbox.delete(0, tk.END)  # Menghapus data lama dari listbox

        for item in data:
            self.delete_listbox.insert(tk.END, item)

    def create_delete_tab(self):
        self.label_delete = tk.Label(self.delete_tab, text="ID Obat untuk dihapus:")
        self.label_delete.grid(row=0, column=0, padx=10, pady=10)

        self.entry_delete = tk.Entry(self.delete_tab)
        self.entry_delete.grid(row=0, column=1, padx=10, pady=10)

        self.button_delete = tk.Button(self.delete_tab, text="Delete", command=self.delete_operation)
        self.button_delete.grid(row=1, column=0, columnspan=2, pady=10)

        # Tambahkan listbox dan scrollbar
        self.listbox_data = tk.Listbox(self.delete_tab, height=10, width=10)
        self.listbox_data.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.delete_tab, orient="vertical", command=self.listbox_data.yview)
        scrollbar.grid(row=2, column=2, pady=10, sticky="ns")
        self.listbox_data.config(yscrollcommand=scrollbar.set)



    def delete_operation(self):
        ID_Obat = self.entry_delete.get()
        delete_operation = DeletePrescription("Clinic A")
        delete_operation.operate(ID_Obat)
        delete_operation.close_connection()

        # Update listbox setelah melakukan operasi delete
        self.update_delete_listbox()


    def create_update_tab(self):
        self.label_update = tk.Label(self.update_tab, text="ID Obat untuk di ambil:")
        self.label_update.grid(row=0, column=0, padx=10, pady=10)

        self.entry_update_old = tk.Entry(self.update_tab)
        self.entry_update_old.grid(row=0, column=1, padx=10, pady=10)

        self.label_new_update = tk.Label(self.update_tab, text="ID Obat yang baru:")
        self.label_new_update.grid(row=1, column=0, padx=10, pady=10)

        self.entry_update_new = tk.Entry(self.update_tab)
        self.entry_update_new.grid(row=1, column=1, padx=10, pady=10)

        self.button_update = tk.Button(self.update_tab, text="Update", command=self.update_operation)
        self.button_update.grid(row=2, column=0, columnspan=2, pady=10)

    def insert_operation(self):
        ID_Obat = self.entry_insert.get()
        insert_operation = InsertPrescription("Clinic A")
        insert_operation.operate(ID_Obat)
        insert_operation.close_connection()

    def delete_operation(self):
        ID_Obat = self.entry_delete.get()
        delete_operation = DeletePrescription("Clinic A")
        delete_operation.operate(ID_Obat)
        delete_operation.close_connection()

    def update_operation(self):
        ID_Obat = self.entry_update_old.get()
        new_ID_Obat = self.entry_update_new.get()
        update_operation = UpdatePrescription("Clinic A")
        update_operation.operate(ID_Obat, new_ID_Obat)
        update_operation.close_connection()

# root = tk.Tk()
# app = PrescriptionApp(root)
# root.mainloop()


# insert_operation = InsertPrescription("Clinic A")
# delete_operation = DeletePrescription("Clinic A")
# update_operation = UpdatePrescription("Clinic A")

# insert_operation.operate("3")
# delete_operation.operate("3333")
# update_operation.operate("3", "3333")

# insert_operation.close_connection()
# delete_operation.close_connection()
# update_operation.close_connection()
