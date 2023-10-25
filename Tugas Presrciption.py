import mysql.connector
import pymysql.cursors

class Prescription:
    def __init__(self, nama_clinic):
        self.nama_clinic = nama_clinic
        self.__ID_obat = {}
        # self._nama = {}

        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='arrivaldophpMyAdmin-0',
            database='merge',
            cursorclass=pymysql.cursors.DictCursor
        )

        if self.conn:
            print('Terhubung ke database MySQL\n')
        else:
            print('Gagal terhubung ke database MySQL\n')

    def insert_ID(self, ID_Obat):
        cursor = self.conn.cursor()
        try:
            insert_query = "INSERT INTO `prescription_data` (`ID_Obat`) VALUES (%s)"
            
            cursor.execute(insert_query, ID_Obat)
            self.conn.commit()
            self.__ID_obat[ID_Obat] = ID_Obat
            print(f"Obat dengan ID: {ID_Obat} telah ditambahkan di list dan database.")
        except mysql.connector.Error as err:
            print(f'Error saat INSERT: {err}')
        finally:
            cursor.close()


    def delete_ID(self, ID_Obat):
        cursor = self.conn.cursor()
        # if ID_Obat in self.__ID_obat:
        #     print(f"Obat dengan ID: {ID_Obat} telah dihapus dari list dan database.")
        #     del self.__ID_obat[ID_Obat]
        # else:
        #     print(f"Obat dengan ID: {ID_Obat} tidak ada dalam list.")

        try:
            delete_query = "DELETE FROM `prescription_data` WHERE `ID_Obat` = %s"
            cursor.execute(delete_query, (ID_Obat,))
            self.conn.commit()
            print(f"Obat dengan ID: {ID_Obat} telah dihapus dari list dan database.")

        except mysql.connector.Error as err:
            print(f'Error saat DELETE: {err}')
        finally:
            cursor.close()

    def update_ID(self, ID_Obat, new_ID_Obat):
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
        except mysql.connector.Error as err:
            print(f'Error saat UPDATE: {err}')
        finally:
            cursor.close()


    def close_connection(self):
        self.conn.close()

# Contoh penggunaan kelas Prescription
clinic = Prescription("Clinic A")

# clinic.insert_ID("2")
# clinic.insert_ID("1002")

clinic.delete_ID("2002")

# clinic.insert_ID("1005")
# clinic.update_ID("1002", "2002")


clinic.close_connection()