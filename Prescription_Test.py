from PrescriptionBase import PrescriptionBase
import pymysql.cursors

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

# Contoh penggunaan
insert_operation = InsertPrescription("Clinic A")
delete_operation = DeletePrescription("Clinic A")
update_operation = UpdatePrescription("Clinic A")

# insert_operation.operate("3")
delete_operation.operate("3333")
# update_operation.operate("3", "3333")

insert_operation.close_connection()
delete_operation.close_connection()
update_operation.close_connection()
