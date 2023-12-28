from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Establish database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="merge"
)

# Create a cursor to execute SQL queries
cursor = db_connection.cursor()

class Person(ABC):
    def __init__(self, patient_id, name, age, gender, prescription):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.prescription = prescription

    @abstractmethod
    def save_to_database(self):
        pass
    @abstractmethod
    def retrieve_patient_by_id(self, patient_id):
        pass
    @abstractmethod
    def update_patient(self):
        pass
    @abstractmethod
    def delete_patient(self):
        pass
    @abstractmethod
    def get_patient_info(self):
        pass

class Patient:
    def __init__(self, patient_id, name, age, gender, prescription):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.prescription = prescription

    def save_to_database(self):
        # Method to save patient details to the database
        sql = "INSERT INTO patient (patient_id, name, age, gender, prescription) VALUES (%s, %s, %s, %s, %s)"
        val = (self.patient_id, self.name, self.age, self.gender, self.prescription)
        cursor.execute(sql, val)
        db_connection.commit()

    @classmethod
    def retrieve_patient_by_id(cls, patient_id):
        # Method to retrieve patient details from the database
        sql = "SELECT patient_id, name, age, gender, prescription FROM patient WHERE patient_id = %s"
        val = (patient_id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            # Unpack the result fetched from the database
            patient_id, name, age, gender, prescription = result
            return cls(patient_id, name, age, gender, prescription)  # Instantiate the class using retrieved values
        else:
            return None

    def update_patient(self):
        # Method to update patient details in the database
        sql = "UPDATE patient SET name = %s, age = %s, gender = %s, prescription = %s WHERE patient_id = %s"
        val = (self.name, self.age, self.gender, self.prescription, self.patient_id)
        cursor.execute(sql, val)
        db_connection.commit()

    def delete_patient(self):
        # Method to delete patient details from the database
        sql = "DELETE FROM patient WHERE patient_id = %s"
        val = (self.patient_id,)
        cursor.execute(sql, val)
        db_connection.commit()

    def get_patient_info(self):
        # Method to get patient information
        print(f"Patient ID: {self.patient_id}\nName: {self.name}\nAge: {self.age}\nGender: {self.gender}\nPrescription: {self.prescription}\n")

# SUBCLASS
class Inpatient(Patient):
    def __init__(self, patient_id, name, age, gender, prescription, room_number, admission_date, discharge_date, treatment_details):
        super().__init__(patient_id, name, age, gender, prescription)
        self.room_number = room_number
        self.admission_date = admission_date
        self.discharge_date = discharge_date
        self.treatment_details = treatment_details

    def assign_room(self, room_number):
        self.room_number = room_number
        print(f"Inpatient {self.patient_id} assigned to Room {self.room_number}")

    def update_treatment_details(self, new_details):
        self.treatment_details = new_details
        print(f"Updated treatment details for Inpatient {self.patient_id}")

    def discharge_patient(self):
        self.discharge_date = "Today"
        print(f"Inpatient {self.patient_id} discharged on {self.discharge_date}")

    def save_to_database(self):
        super().save_to_database()  # Call the save_to_database method of the parent class

        # Save specific Inpatient details to the database
        sql = "UPDATE patient SET room_number = %s, admission_date = %s, discharge_date = %s, treatment_details = %s WHERE patient_id = %s"
        val = (self.room_number, self.admission_date, self.discharge_date, self.treatment_details, self.patient_id)
        cursor.execute(sql, val)
        db_connection.commit()

class Outpatient(Patient):
    def __init__(self, patient_id, name, age, gender, prescription, appointment_date, appointment_time, visiting_doctor):
        super().__init__(patient_id, name, age, gender, prescription)
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.visiting_doctor = visiting_doctor

    def schedule_appointment(self, date, time, doctor):
        self.appointment_date = date
        self.appointment_time = time
        self.visiting_doctor = doctor
        print(f"Outpatient {self.patient_id} scheduled an appointment for {self.appointment_date} at {self.appointment_time} with Dr. {self.visiting_doctor}")

    def save_to_database(self):
        super().save_to_database()  # Call the save_to_database method of the parent class

        # Save specific Outpatient details to the database
        sql = "UPDATE patient SET appointment_date = %s, appointment_time = %s, visiting_doctor = %s WHERE patient_id = %s"
        val = (self.appointment_date, self.appointment_time, self.visiting_doctor, self.patient_id)
        cursor.execute(sql, val)
        db_connection.commit()    

class PatientManagementGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Patient Management System")
        self.root.configure(bg="lightblue")

        button_frame = tk.Frame(root, bg="lightblue")
        button_frame.pack(side="top", padx=10, pady=10)

        button_style = {'font': ('Arial', 12), 'fg': 'white', 'bg': '#2980b9', 'activebackground': '#2c3e50', 'width': 15}

        self.button_add = tk.Button(button_frame, text="Add Patient", command=self.add_patient, **button_style)
        self.button_add.pack(side="left", padx=10)

        self.button_get = tk.Button(button_frame, text="Retrieve Patient", command=self.retrieve_patient, **button_style)
        self.button_get.pack(side="left", padx=10)

        self.button_update = tk.Button(button_frame, text="Update Patient", command=self.update_patient, **button_style)
        self.button_update.pack(side="left", padx=10)

        self.button_delete = tk.Button(button_frame, text="Delete Patient", command=self.delete_patient, **button_style)
        self.button_delete.pack(side="left", padx=10)

        self.button_add_inpatient = tk.Button(button_frame, text="Add Inpatient", command=self.add_inpatient, **button_style)
        self.button_add_inpatient.pack(side="left", padx=10)

        self.button_add_outpatient = tk.Button(button_frame, text="Add Outpatient", command=self.add_outpatient, **button_style)
        self.button_add_outpatient.pack(side="left", padx=10)

        self.button_logout = tk.Button(button_frame, text="Logout", command=self.logout, **button_style)
        self.button_logout.pack(side="left", padx=10)

        # Create a Treeview widget to display patient details
        self.tree = ttk.Treeview(
            root,
            columns=("Patient ID", "Name", "Age", "Gender", "Prescription", "Room Number", "Admission Date", "Discharge Date", "Treatment Date", "Appointment Date", "Appointment Time", "Visiting Doctor"),
            show="headings",
            style="Custom.Treeview"
        )

        # Set headings
        self.tree.heading("Patient ID", text="Patient ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Prescription", text="Prescription")
        self.tree.heading("Room Number", text="Room Number")
        self.tree.heading("Admission Date", text="Admission Date")
        self.tree.heading("Discharge Date", text="Discharge Date")
        self.tree.heading("Treatment Date", text="Treatment Date")
        self.tree.heading("Appointment Date", text="Appointment Date")
        self.tree.heading("Appointment Time", text="Appointment Time")
        self.tree.heading("Visiting Doctor", text="Visiting Doctor")

        # Set column sizes
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in self.tree["columns"]:
            self.tree.column(col, width=135, stretch=tk.NO)

        # Configure scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=20, background="#3498db", foreground="white",
                        fieldbackground="#3498db", highlightthickness=0, bd=0)
        self.tree.pack(expand=True, fill="both")
        self.load_data_into_table()
    
    def add_patient(self):
        # Placeholder functionality for adding a patient
        add_patient_window = tk.Toplevel(self.root)
        add_patient_window.title("Add New Patient")

        # Create labels and entry widgets for patient details
        tk.Label(add_patient_window, text="Patient ID: ").pack()
        patient_id_entry = tk.Entry(add_patient_window)
        patient_id_entry.pack()

        tk.Label(add_patient_window, text="Name: ").pack()
        name_entry = tk.Entry(add_patient_window)
        name_entry.pack()

        tk.Label(add_patient_window, text="Age: ").pack()
        age_entry = tk.Entry(add_patient_window)
        age_entry.pack()

        tk.Label(add_patient_window, text="Gender: ").pack()
        gender_entry = tk.Entry(add_patient_window)
        gender_entry.pack()

        tk.Label(add_patient_window, text="Prescription: ").pack()
        prescription_entry = tk.Entry(add_patient_window)
        prescription_entry.pack()

        # Upon submission, collect the entered data and process it
        def submit_patient():
            patient_id = patient_id_entry.get()
            name = name_entry.get()
            age = age_entry.get()
            gender = gender_entry.get()
            prescription = prescription_entry.get()

            # Create a new Patient object and save it to the database
            patient = Patient(patient_id, name, age, gender, prescription)
            patient.save_to_database()
            messagebox.showinfo("Success", "Patient information added successfully!")

        # Button to submit the patient details
        submit_button = tk.Button(add_patient_window, text="Submit", command=submit_patient)
        submit_button.pack()

    def retrieve_patient(self):
        # Placeholder functionality for retrieving a patient
        retrieve_patient_window = tk.Toplevel(self.root)
        retrieve_patient_window.title("Retrieve Patient")

        # Create fields for searching (e.g., ID, name, etc.)
        tk.Label(retrieve_patient_window, text="Enter Patient ID:").pack()
        patient_id_entry = tk.Entry(retrieve_patient_window)
        patient_id_entry.pack()

        # Function to retrieve patient details based on the entered ID
        def retrieve_patient_details():
            patient_id_to_retrieve = patient_id_entry.get()
        
            # Create an instance of the Patient class
            patient_obj = Patient("", "", "", "", "")  # Provide default values for the constructor
        
            # Retrieve patient details using the instance
            patient = patient_obj.retrieve_patient_by_id(patient_id_to_retrieve)

            if patient:
                # Display retrieved patient information in a message box or label
                patient_info = f"Patient ID: {patient.patient_id}\nName: {patient.name}\nAge: {patient.age}\nGender: {patient.gender}\nPrescription: {patient.prescription}"
                messagebox.showinfo("Patient Details", patient_info)
            else:
                messagebox.showinfo("Patient Not Found", "Patient not found for the provided ID.")

        # Button to submit and retrieve patient information
        submit_button = tk.Button(retrieve_patient_window, text="Retrieve", command=retrieve_patient_details)
        submit_button.pack()

        
    def update_patient(self):
        # Placeholder functionality for updating a patient
        update_patient_window = tk.Toplevel(self.root)
        update_patient_window.title("Update Patient")

        # Create fields to update patient details
        tk.Label(update_patient_window, text="Enter Patient ID:").pack()
        patient_id_entry = tk.Entry(update_patient_window)
        patient_id_entry.pack()

        tk.Label(update_patient_window, text="New Name:").pack()
        new_name_entry = tk.Entry(update_patient_window)
        new_name_entry.pack()

        tk.Label(update_patient_window, text="New Age:").pack()
        new_age_entry = tk.Entry(update_patient_window)
        new_age_entry.pack()

        tk.Label(update_patient_window, text="New Gender:").pack()
        new_gender_entry = tk.Entry(update_patient_window)
        new_gender_entry.pack()

        tk.Label(update_patient_window, text="New Prescription:").pack()
        new_prescription_entry = tk.Entry(update_patient_window)
        new_prescription_entry.pack()

        # Function to update patient details based on the entered information
        def update_patient_details():
            patient_id_to_update = patient_id_entry.get()
        
            # Retrieve patient details using the entered ID
            patient = Patient.retrieve_patient_by_id(patient_id_to_update)

            if patient:
                new_name = new_name_entry.get()
                new_age = new_age_entry.get()
                new_gender = new_gender_entry.get()
                new_prescription = new_prescription_entry.get()

                # Update the patient object with new values
                patient.name = new_name
                patient.age = new_age
                patient.gender = new_gender
                patient.prescription = new_prescription

                patient.update_patient()
                messagebox.showinfo("Success", "Patient information updated successfully!")
            else:
                messagebox.showinfo("Patient Not Found", "Patient not found for the provided ID.")

        # Button to submit and update patient information
        submit_button = tk.Button(update_patient_window, text="Update", command=update_patient_details)
        submit_button.pack()

    def delete_patient(self):
        # Placeholder functionality for deleting a patient
        delete_patient_window = tk.Toplevel(self.root)
        delete_patient_window.title("Delete Patient")

        # Create a label and entry field to specify the patient ID to be deleted
        tk.Label(delete_patient_window, text="Enter Patient ID to Delete:").pack()
        patient_id_entry = tk.Entry(delete_patient_window)
        patient_id_entry.pack()

        # Function to delete the patient based on the entered ID
        def delete_patient_record():
            patient_id_to_delete = patient_id_entry.get()
            patient = Patient.retrieve_patient_by_id(patient_id_to_delete)

            if patient:
                patient.delete_patient()
                messagebox.showinfo("Success", "Patient information deleted successfully!")
            else:
                messagebox.showinfo("Patient Not Found", "Patient not found for the provided ID.")

        # Button to confirm deletion
        submit_button = tk.Button(delete_patient_window, text="Delete", command=delete_patient_record)
        submit_button.pack()

    def add_inpatient(self):
        # Placeholder functionality for adding an inpatient
        add_inpatient_window = tk.Toplevel(self.root)
        add_inpatient_window.title("Add Inpatient")

        # Create form fields for inpatient details
        tk.Label(add_inpatient_window, text="Patient ID:").pack()
        patient_id_entry = tk.Entry(add_inpatient_window)
        patient_id_entry.pack()

        tk.Label(add_inpatient_window, text="Name:").pack()
        name_entry = tk.Entry(add_inpatient_window)
        name_entry.pack()

        tk.Label(add_inpatient_window, text="Age:").pack()
        age_entry = tk.Entry(add_inpatient_window)
        age_entry.pack()

        tk.Label(add_inpatient_window, text="Gender:").pack()
        gender_entry = tk.Entry(add_inpatient_window)
        gender_entry.pack()

        tk.Label(add_inpatient_window, text="Prescription:").pack()
        prescription_entry = tk.Entry(add_inpatient_window)
        prescription_entry.pack()

        tk.Label(add_inpatient_window, text="Room Number:").pack()
        room_number_entry = tk.Entry(add_inpatient_window)
        room_number_entry.pack()

        tk.Label(add_inpatient_window, text="Admission Date:").pack()
        admission_date_entry = tk.Entry(add_inpatient_window)
        admission_date_entry.pack()

        tk.Label(add_inpatient_window, text="Discharge Date:").pack()
        discharge_date_entry = tk.Entry(add_inpatient_window)
        discharge_date_entry.pack()

        tk.Label(add_inpatient_window, text="Treatment Details:").pack()
        treatment_details_entry = tk.Entry(add_inpatient_window)
        treatment_details_entry.pack()

        # Function to add the inpatient details to the database
        def add_inpatient_record():
            inpatient_id = patient_id_entry.get()
            inpatient_name = name_entry.get()
            inpatient_age = age_entry.get()
            inpatient_gender = gender_entry.get()
            inpatient_prescription = prescription_entry.get()
            inpatient_room_number = room_number_entry.get()
            inpatient_admission_date = admission_date_entry.get()
            inpatient_discharge_date = discharge_date_entry.get()
            inpatient_treatment_details = treatment_details_entry.get()

            # Create a new Inpatient object and save it to the database
            inpatient = Inpatient(
                inpatient_id, inpatient_name, inpatient_age, inpatient_gender, inpatient_prescription,
                inpatient_room_number, inpatient_admission_date, inpatient_discharge_date, inpatient_treatment_details
            )
            inpatient.save_to_database()
            messagebox.showinfo("Success", "Inpatient information added successfully!")

        # Button to submit the inpatient details
        submit_button = tk.Button(add_inpatient_window, text="Submit", command=add_inpatient_record)
        submit_button.pack()

    def add_outpatient(self):
        # Placeholder functionality for adding an outpatient
        add_outpatient_window = tk.Toplevel(self.root)
        add_outpatient_window.title("Add Outpatient")

        # Create form fields for outpatient details
        tk.Label(add_outpatient_window, text="Patient ID:").pack()
        patient_id_entry = tk.Entry(add_outpatient_window)
        patient_id_entry.pack()

        tk.Label(add_outpatient_window, text="Name:").pack()
        name_entry = tk.Entry(add_outpatient_window)
        name_entry.pack()

        tk.Label(add_outpatient_window, text="Age:").pack()
        age_entry = tk.Entry(add_outpatient_window)
        age_entry.pack()

        tk.Label(add_outpatient_window, text="Gender:").pack()
        gender_entry = tk.Entry(add_outpatient_window)
        gender_entry.pack()

        tk.Label(add_outpatient_window, text="Prescription:").pack()
        prescription_entry = tk.Entry(add_outpatient_window)
        prescription_entry.pack()

        tk.Label(add_outpatient_window, text="Appointment Date:").pack()
        appointment_date_entry = tk.Entry(add_outpatient_window)
        appointment_date_entry.pack()

        tk.Label(add_outpatient_window, text="Appointment Time:").pack()
        appointment_time_entry = tk.Entry(add_outpatient_window)
        appointment_time_entry.pack()

        tk.Label(add_outpatient_window, text="Visiting Doctor:").pack()
        visiting_doctor_entry = tk.Entry(add_outpatient_window)
        visiting_doctor_entry.pack()

        # Function to add the outpatient details to the database
        def add_outpatient_record():
            outpatient_id = patient_id_entry.get()
            outpatient_name = name_entry.get()
            outpatient_age = age_entry.get()
            outpatient_gender = gender_entry.get()
            outpatient_prescription = prescription_entry.get()
            outpatient_appointment_date = appointment_date_entry.get()
            outpatient_appointment_time = appointment_time_entry.get()
            outpatient_visiting_doctor = visiting_doctor_entry.get()

            # Create a new Outpatient object and save it to the database
            outpatient = Outpatient(
                outpatient_id, outpatient_name, outpatient_age, outpatient_gender, outpatient_prescription,
                outpatient_appointment_date, outpatient_appointment_time, outpatient_visiting_doctor
            )
            outpatient.save_to_database()
            messagebox.showinfo("Success", "Outpatient information added successfully!")

        # Button to submit the outpatient details
        submit_button = tk.Button(add_outpatient_window, text="Submit", command=add_outpatient_record)
        submit_button.pack()

    def logout(self):
        # Perform logout actions here if needed
        self.root.destroy()  # Close the application window 

    # Close the cursor and database connection when done
    def close_connection(self):
        self.cursor.close()
        self.db_connection.close()

    def load_data_into_table(self):
        # Fetch data from the database
        cursor.execute("SELECT * FROM patient")
        data = cursor.fetchall()

        # Clear existing data in the Treeview
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Insert fetched data into the Treeview
        if data:
            for row in data:
                self.tree.insert("", "end", values=row)     
            
if __name__ == "__main__":
    # Initialize the Tkinter application
    root = tk.Tk()
    app = PatientManagementGUI(root)  # Passing only the root
    root.mainloop()


