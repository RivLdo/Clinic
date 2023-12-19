import mysql.connector

db = mysql.connector.connect(
    # 
)

class Appointment:
    def __init__(self, db_connection):
        self._db = db_connection
        self._cursor = self._db.cursor()
        self.__id_counter = 1

    def _generate_id(self):
        new_id = self.__id_counter
        self.__id_counter += 1
        return new_id
    
    def create_appointment(self):
        print("Pembuatan Appointment:")
        patient_name = input("Masukkan nama pasien: ")
        doctor_name = input("Masukkan nama dokter: ")
        date = input("Masukkan tanggal (YYYY-MM-DD): ")
        description = input("Masukkan deskripsi: ")
        time = input("Masukkan waktu pertemuan (HH:MM):")

        sql = "INSERT INTO appointments (patient_name, doctor_name, date, time, description) VALUES (%s, %s, %s, %s, %s)"
        values = (patient_name, doctor_name, date, time, description)

        self._cursor.execute(sql, values)
        self._db.commit()

        print("Appointment sukses dibuat.\n")

    def reschedule_appointment(self):
        print("Rescheduling sebuah Appointment")
        appointment_id = int(input("Masukkan ID appointment untuk reschedule: "))

        new_date = input("Masukkan tanggal baru (YYYY-MM-DD): ")
        new_time = input("Masukkan waktu pertemuan baru (HH:MM): ")

        sql = "UPDATE appointments SET date = %s, time = %s WHERE id = %s"
        values = (new_date, new_time, appointment_id)

        self._cursor.execute(sql, values)
        self._db.commit()

        if self._cursor.rowcount > 0:
            print(f"Appoinment dengan ID {appointment_id} berhasil direschedule.\n")
        else:
            print(f"Appoinment dengan ID {appointment_id} tidak ditemukan.\n")

    def cancel_appointment(self):
        print("Pembatalan Appointment")
        appointment_id = int(input("Masukkan ID appointment untuk dibatalkan: "))

        sql = "DELETE FROM appointments WHERE id = %s"
        values = (appointment_id,)

        self._cursor.execute(sql, values)
        self._db.commit()

        if self._cursor.rowcount > 0:
            print(f"appoinment dengan ID {appointment_id} berhasil dibatalkan.\n")
        else:
            print(f"appoinment dengan ID {appointment_id} tidak ditemukan.\n")

    def list_appointments(self):
        print("{:<4} {:<20} {:<20} {:<15} {:<15} {:<40}".format("ID", "Patient Name", "Doctor Name", "Date", "Time", "Description"))
        print("=" * 95)

        sql = "SELECT id, patient_name, doctor_name, date, time, description FROM appointments"
        self._cursor.execute(sql)
        appointments = self._cursor.fetchall()
        for appointment in appointments:
            appointment_id, patient_name, doctor_name, date, time, description = appointment
            formatted_date = date.strftime('%Y-%m-%d')
            formatted_time = str(time)
            print("{:<4} {:<20} {:<20} {:<15} {:<15} {:<40}".format(appointment_id, patient_name, doctor_name, formatted_date, formatted_time, description))

    def close_connection(self):
        self._cursor.close()
        self._db.close()
        print("Terima kasih. Semoga sehat selalu!\n")

if __name__ == '__main__':
    manager_appointment = Appointment(db)

    while True:
        print("Menu:")
        print("1. Pembuatan Appointment")
        print("2. Reschedule Appointment")
        print("3. Pembatalan Appointment")
        print("4. List Appointments")
        print("5. Exit")
        choice = input("Select an action (1/2/3/4/5): ")

        if choice == '1':
            manager_appointment.create_appointment()
        elif choice == '2':
            manager_appointment.reschedule_appointment()
        elif choice == '3':
            manager_appointment.cancel_appointment()
        elif choice == '4':
            manager_appointment.list_appointments()
        elif choice == '5':
            manager_appointment.close_connection()
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

# CREATE TABLE appointments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     patient_name VARCHAR(255) NOT NULL,
#     doctor_name VARCHAR(255) NOT NULL,
#     date DATE NOT NULL,
#     time TIME NOT NULL,
#     description TEXT
# );
