from abc import ABC, abstractmethod
from Connection import conn_to_database

class PrescriptionBase(ABC):
    def __init__(self, nama_clinic):
        self.nama_clinic = nama_clinic
        self.__ID_obat = {}
        self.conn = conn_to_database()

        if self.conn:
            print('Terhubung ke database MySQL\n')
        else:
            print('Gagal terhubung ke database MySQL\n')

    @abstractmethod
    def operate(self, ID_Obat, new_ID_Obat):
        pass

    def close_connection(self):
        self.conn.close()