# using the mysql.connector library
import mysql.connector

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "kelompok 5"
) 

# Create a cursor to execute SQL queries
cursor = db_connection.cursor()


class Patient:
#def itu method
    def __init__(self, patient_id, name, age, gender, prescription):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.prescription = prescription

    def get_patient_id(self):
        return self.patient_id

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_gender(self):
        return self.gender
    
    def get_prescription(self):
        return self.prescription


# Define the SQL query to INSERT to patient
    def save_to_database(self):
        sql = "INSERT INTO patient (patient_id, name, age, gender, prescription) VALUES (%s, %s, %s, %s, %s)"
        val = (self.patient_id, self.name, self.age, self.gender, self.prescription)
        cursor.execute(sql, val)
        db_connection.commit()


    # Define the SQL query to SELECT a patient by patient_id
    def retrieve_patient_by_id(patient_id):
        sql = "SELECT * FROM patient WHERE patient_id = %s"
        val = (patient_id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            return Patient(*result)
        else:
            return None

    # Define the SQL query to UPDATE a patient's information
    def update_patient(self):
        sql = "UPDATE patient SET name = %s, age = %s, gender = %s, prescription = %s WHERE patient_id = %s"
        val = (self.name, self.age, self.gender, self.prescription, self.patient_id)
        cursor.execute(sql, val)
        db_connection.commit()


    # Define the SQL query to DELETE a patient by patient_id
    def delete_patient(self):
        sql = "DELETE FROM patient WHERE patient_id = %s"
        val = (self.patient_id,)
        cursor.execute(sql, val)
        db_connection.commit()


#utk print data
    def get_patient_info(self):
        print (f"Patient ID: {self.patient_id} \nName: {self.name} \nAge: {self.age} \nGender: {self.gender} \nPrescription: {self.prescription} \n")   


if __name__ == "__main__":
    patient_arr = []

    while True:
        print("\nMENU:")
        print("\t1. Add new patient record")
        print("\t2. Retrieve patient details")
        print("\t3. Update patient details")
        print("\t4. Delete patient record")
        print("\t5. LOGOUT")


        choice = input("\nEnter your choice: ")

        if choice == '1':
            patient_id = input("\tEnter patient ID: ")
            name = input("\tEnter patient name: ")
            age = input("\tEnter patient age: ")
            gender = input("\tEnter patient gender: ")
            prescription = input("\tEnter prescription: ")

            # Create a new 'Patient' object and save it to the database
            patient = Patient(patient_id, name, age, gender, prescription) #obj
            patient.save_to_database()
            # Append the 'Patient' object to the 'patient_arr' list for further processing or storage
            patient_arr.append(patient)
            print("\n\tPatient information has been successfully added!")


        elif choice == '2':
            # Retrieve patient details by patient_id
            patient_id_to_select = input("\n\tPlease enter the Patient's ID to retrieve their information: ")
            patient = Patient.retrieve_patient_by_id(patient_id_to_select) #obj
            
            if patient:
                print("\n\tPatient Detail:")
                print(f"\tPatient ID: {patient.patient_id}")
                print(f"\tPatient Name: {patient.name}")
                print(f"\tPatient Age: {patient.age}")
                print(f"\tPatient Gender: {patient.gender}")
                print(f"\tPrescription: {patient.prescription}")
            else:
                print("\n\tPatient not found for the provided Patient ID.")

        elif choice == '3':
            # Update patient details
            patient_id_to_update = input("\n\tEnter the Patient ID you want to update: ")
            patient = Patient.retrieve_patient_by_id(patient_id_to_update) #obj
            if patient:
                new_name = input("\tEnter the new name: ")
                new_age = input("\tEnter the new age: ")
                new_gender = input("\tEnter the new gender: ")
                new_prescription = input("\tEnter the new prescription: ")
                # Update patient details
                patient.name = new_name
                patient.age = new_age
                patient.gender = new_gender
                patient.prescription = new_prescription
                patient.update_patient()
                print("\n\tPatient information has been successfully updated!")
            else:
                print("\n\tPatient not found for the provided Patient ID.")

        elif choice == '4':
            # Delete patient details
            patient_id_to_delete = input("\n\tEnter the Patient ID you want to delete: ")
            patient = Patient.retrieve_patient_by_id(patient_id_to_delete) #obj
            if patient:
                patient.delete_patient()
                print("\n\tPatient details deleted!")
            else:
                print("\n\tPatient not found for the provided Patient ID.")

        elif choice == '5':
            print("\nSession ended.\n")
            break

        else:
            print("\nInvalid choice. Please try again.\n")

    
# Close the cursor and database connection when done
cursor.close()
db_connection.close()
 






