# Import the 'mysql.connector' library, which is used to connect to and interact with MySQL databases
import mysql.connector

# Establish a connection to a MySQL database using the mysql.connector library
db =mysql.connector.connect(
    # 
) 

# Create a database cursor to interact with the database
cur = db.cursor()

class Doctor:
    def __init__(self, doc_ID=None, doc_name=None, doc_gender=None, doc_mobile=None, doc_specialization=None, doc_annualSal=None, doc_ID_to_select=None, doc_ID_to_delete=None):
        if doc_ID is not None:
            self.doc_ID = doc_ID
            self.doc_name = doc_name
            self.doc_gender = doc_gender
            self.__doc_mobile = doc_mobile
            self.doc_specialization = doc_specialization
            self.__doc_annualSal = doc_annualSal
        elif doc_ID_to_select is not None:
            self.doc_ID_to_select = doc_ID_to_select
        elif doc_ID_to_delete is not None:
            self.doc_ID_to_delete = doc_ID_to_delete

    # Defining method to return attribute value
    def get_doc_ID(self):
        return self.doc_ID
    def get_doc_name(self):
        return self.doc_name
    def get_doc_gender(self):
        return self.doc_gender
    def get_doc_mobile(self):
        return self.__doc_mobile
    def get_doc_specialization(self):
        return self.doc_specialization
    def get_doc_annualSal(self):
        return self.__doc_annualSal
    
    # Define sql query to INSERT to doctor
    def insert_to_database(self):
        sql = "INSERT INTO doctor (doc_ID, doc_name, doc_gender, doc_mobile, doc_specialization, doc_annualSal) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (self.doc_ID, self.doc_name, self.doc_gender, self.__doc_mobile, self.doc_specialization, self.__doc_annualSal)
    
        # Execute INSERT sql query
        cur.execute(sql, val)
        db.commit()
        print(f"\n\t{cur.rowcount} Record added into table!")

    # Define sql query to SELECT doctor details
    def select_from_database(self):
        sql = "SELECT * FROM doctor WHERE doc_ID = %s"
        val = (self.doc_ID, self.doc_name, self.doc_gender, self.__doc_mobile, self.doc_specialization, self.__doc_annualSal)

        # Execute SELECT sql query
        cur.execute(sql, val)
        db.commit()
    
    # Define sql query to DELETE doctor details
    def delete_from_database(self):
        sql = "DELETE FROM doctor WHERE doc_ID = %s"
        # Replace self.doc_ID with the actual identifier 
        val = (self.doc_ID_to_delete,) 

        cur.execute(sql, val)
        db.commit()
        

# Code in this block will only run if this script is the main program
if __name__ == "__main__":
    # Create an empty list to store doctor information or objects
    doctor_arr = []

    while True:
        print ("\nMENU:")
        print ("\t1.Add doctor details")
        print ("\t2.Get doctor details")
        print ("\t3.Update doctor details")
        print ("\t4.Delete doctor details")
        print ("\t5.EXIT")

        choice=input("\nEnter your choice: ")
        if choice=='1':
            print("\n\t------Please Enter Doctor Information------")
            doc_ID=input ("\tEnter doctor ID : ")
            doc_name=input ("\tEnter doctor name : ")
            doc_gender=input ("\tEnter doctor gender : ")
            doc_mobile=input ("\tEnter doctor mobile number : ")
            doc_specialization=input ("\tEnter doctor specialization : ")
            doc_annualSal=input ("\tEnter doctor annual salary : ")

            # Create a Doctor object called 'doctor' with the specified doctor information
            doctor = Doctor(doc_ID, doc_name, doc_gender, doc_mobile, doc_specialization, doc_annualSal)

            # Call the insert_to_database method of the Doctor object to add the doctor's details to the database
            doctor.insert_to_database()

            # Append the 'Doctor' object to the 'doctor_arr' list for further processing or storage
            doctor_arr.append(doctor)

        elif choice == '2':
            # SELECT to display doctor details
            doc_ID_to_select = input("\tProvide the Doctor ID to access information: ")
            cur.execute("SELECT * FROM doctor WHERE doc_ID = %s", (doc_ID_to_select,))
            result = cur.fetchone()     # Retrieve the next row (result) from the database cursor's result set

            if result:
                print("\n\t------Doctor Information------")
                print("\t--------------------------------")
                print(f"\tDoctor ID: {result[0]}")
                print(f"\tDoctor Name: {result[1]}")
                print(f"\tDoctor Gender: {result[2]}")
                print(f"\tDoctor Mobile No: {result[3]}")
                print(f"\tDoctor Specialization: {result[4]}")
                print(f"\tDoctor Salary per year: {result[5]}")
                print("\t--------------------------------")
            else:
                print("\tNo record found.")
                
                # Create a Doctor object called 'select' for selecting a specific doctor's details
                select = Doctor(doc_ID_to_select)

                # Call the select_from_database method of the Doctor object to retrieve the doctor's information
                select.select_from_database()
 
        elif choice == '3':
            # UPDATING doctors details
            doc_ID_to_update = input("\t\nPlease enter Doctor ID to update: ")
            cur.execute("SELECT * FROM doctor WHERE doc_ID = %s", (doc_ID_to_update,))
            result = cur.fetchone()     # Retrieve the next row (result) from the database cursor's result set 

            # Prompt the user for updated details
            new_name = input("\n\tNew name: ")
            new_gender = input("\tNew gender: ")
            new_mobile = input("\tNew mobile number: ")
            new_specialization = input("\tNew specialization: ")
            new_annualSal = input("\tNew salary per year: ")   

            # Define sql query to UPDATE doctor record
            sql = "UPDATE doctor SET doc_name = %s, doc_gender = %s, doc_mobile = %s, doc_specialization = %s, doc_annualSal = %s WHERE doc_ID = %s"
            val = (new_name, new_gender, new_mobile, new_specialization, new_annualSal, doc_ID_to_update)
            
            # Execute the SQL update query
            cur.execute(sql, val)
            db.commit()
            print(f"\nDoctor record with ID {doc_ID_to_update} is successfully updated!")

        elif choice == '4':
            # DELETING doctor details 
            doc_ID_to_delete = input("\t\nEnter the Doctor ID you want to delete: ")

            # Create a Doctor object called 'delete' to delete a specific doctor's details 
            delete = Doctor(doc_ID_to_delete=doc_ID_to_delete)

            # Call the delete_from_database method of the Doctor object to initiate the deletion
            delete.delete_from_database()

            print(f"\nDoctor record with ID {doc_ID_to_delete} is successfully deleted!")

        elif choice == '5':
            print("\n\t-----------------------------------")
            print("\t  Thank you for using the system !")
            print("\t-----------------------------------\n")
            break

        else:
            print ("\n------  ERROR !!!  ------\n")    


#close
cur.close()
db.close()
