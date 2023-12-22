import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from abc import ABC, abstractmethod

# Establish a connection to a MySQL database using the pymysql library
db =pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '12345',
    database = 'merge'
) 

# Create a database cursor to interact with the database
cur = db.cursor()

class Doctor(ABC):
    def __init__(self, doc_ID=None, doc_name=None, doc_gender=None, doc_mobile=None, doc_specialization=None, doc_annualSal=None, 
                 doc_ID_to_select=None, doc_ID_to_delete=None):
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

    @abstractmethod
    def insert_to_database(self):
        pass
    @abstractmethod
    def select_from_database(self):
        pass
    @abstractmethod
    def update_in_database(self, new_values):
        pass
    @abstractmethod
    def delete_from_database(self):
        pass        

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
        result = cur.fetchone()
        db.commit()
    
    # Define sql query to DELETE doctor details
    def delete_from_database(self):
        sql = "DELETE FROM doctor WHERE doc_ID = %s"
        # Replace self.doc_ID with the actual identifier 
        val = (self.doc_ID_to_delete,) 

        cur.execute(sql, val)
        db.commit()

# Class Anak 1: InternDoctor
class InternDoctor(Doctor):
    def __init__(self, doc_ID=None, doc_name=None, doc_gender=None, doc_mobile=None, doc_specialization=None, doc_annualSal=None,
                 doc_ID_to_select=None, doc_ID_to_delete=None, hospital_name=None, intern_year=None):
        super().__init__(doc_ID, doc_name, doc_gender, doc_mobile, doc_specialization, doc_annualSal,
                         doc_ID_to_select, doc_ID_to_delete)
        self.hospital_name = hospital_name
        self.intern_year = intern_year

    def get_hospital_name(self):
        return self.hospital_name
    def get_intern_year(self):
        return self.intern_year
    
        # Override abstract methods
    def insert_to_database(self):
        super().insert_to_database()
    def select_from_database(self):
        super().select_from_database()
    def delete_from_database(self):
        super().delete_from_database()

# Class Anak 2: SeniorDoctor
class SeniorDoctor(Doctor):
    def __init__(self, doc_ID=None, doc_name=None, doc_gender=None, doc_mobile=None, doc_specialization=None, doc_annualSal=None,
                 doc_ID_to_select=None, doc_ID_to_delete=None, hospital_name=None, retirement_year=None):
        super().__init__(doc_ID, doc_name, doc_gender, doc_mobile, doc_specialization, doc_annualSal,
                         doc_ID_to_select, doc_ID_to_delete)
        self.hospital_name = hospital_name
        self.retirement_year = retirement_year

    # Additional method for ClinicDoctor
    def get_hospital_name(self):
        return self.hospital_name
    def get_retirement_year(self):
        return self.retirement_year
    
        # Override abstract methods
    def insert_to_database(self):
        super().insert_to_database()
    def select_from_database(self):
        super().select_from_database()
    def delete_from_database(self):
        super().delete_from_database()

class DocGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Doctor Management System")
        self.master.configure(bg="#3498db")

        # Create a Frame for buttons
        button_frame = tk.Frame(master, bg="#3498db")
        button_frame.pack(side="top", padx=10, pady=10)

        button_style = {'font': ('Arial', 12), 'fg': 'white', 'bg': '#2980b9', 'activebackground': '#2c3e50', 'width': 15}
        self.button_add = tk.Button(button_frame, text="Add Doctor", command=self.add_GUI, **button_style)
        self.button_add.pack(side="left", padx=10)

        self.button_get = tk.Button(button_frame, text="Get Doctor", command=self.get_GUI, **button_style)
        self.button_get.pack(side="left", padx=10)

        self.button_update = tk.Button(button_frame, text="Update Doctor", command=self.update_GUI, **button_style)
        self.button_update.pack(side="left", padx=10)

        self.button_delete = tk.Button(button_frame, text="Delete Doctor", command=self.delete_GUI, **button_style)
        self.button_delete.pack(side="left", padx=10)

        self.button_exit = tk.Button(button_frame, text="EXIT", command=self.close_connection_and_exit, **button_style)
        self.button_exit.pack(side="left", padx=10)

        # Create a Treeview widget to display the doctor details
        self.tree = ttk.Treeview(
            master,
            columns=("ID", "Name", "Gender", "Mobile", "Specialization", "Salary", "Hospital", "Intern Year", "Retirement Year"),
            show="headings",
            style="Custom.Treeview"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Mobile", text="Mobile")
        self.tree.heading("Specialization", text="Specialization")
        self.tree.heading("Salary", text="Salary")
        self.tree.heading("Hospital", text="Hospital")
        self.tree.heading("Intern Year", text="Intern Year")
        self.tree.heading("Retirement Year", text="Retirement Year")

        heading_style = {'font': ('Arial', 12, 'bold'), 'anchor': 'center', 'foreground': 'white', 'background': '#3498db'}
        for col in self.tree["columns"]:
            # self.tree.heading(col, text=col)
            self.tree.tag_configure(f"{col}_tag", **heading_style)
            self.tree.heading(col, text=col, anchor='center', command=lambda c=col: self.sort_column(c), image="")
            # self.tree.column(col, width=140, stretch=tk.NO)

        # Set column sizes and adjust the style
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in self.tree["columns"]:
            self.tree.column(col, width=135, stretch=tk.NO)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=20, background="#3498db", foreground="white",
                        fieldbackground="#3498db", highlightthickness=0, bd=0)
        self.tree.pack(expand=True, fill="both")
        self.load_data_into_table()

    def sort_column(self, col, reverse=False):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

    def load_data_into_table(self):
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        cur.execute("SELECT * FROM doctor")
        results = cur.fetchall()

        for row in results:
            self.tree.insert("", "end", values=row)

    def add_GUI(self):
        #Create a new window for choosing doctor types
        add_window = tk.Toplevel(self.master)
        add_window.title("Choose Doctor Type")
        add_window.geometry("300x200")
        add_window.configure(bg="#7FB3D5")

        self.label = tk.Label(add_window, text="Please select type of Doctor", font=("Arial", 11))
        self.label.pack(pady=20)

        self.button_choice = tk.Button(add_window, text="Intern Doctor", command=self.add_intern_GUI)
        self.button_choice.pack(pady=15)

        self.button_choice2 = tk.Button(add_window, text="Senior Doctor", command=self.add_senior_GUI)
        self.button_choice2.pack(pady=15)

    def add_intern_GUI(self):
        #Create a new window for adding Intern Doctor
        intern_add_window = tk.Toplevel(self.master)
        intern_add_window.title("Adding Intern Doctor Details")
        intern_add_window.geometry("400x450")
        intern_add_window.configure(bg="#7FB3D5")
        tk.Label(intern_add_window, text="Please add Intern Doctor details", font=("Arial", 11), bg="#7FB3D5").grid(row=0, columnspan=2, pady=10)

        label_entries = [
            ("Doctor ID:", tk.Entry(intern_add_window)),
            ("Doctor Name:", tk.Entry(intern_add_window)),
            ("Doctor Gender:", tk.Entry(intern_add_window)),
            ("Doctor Mobile Number:", tk.Entry(intern_add_window)),
            ("Doctor Specialization:", tk.Entry(intern_add_window)),
            ("Doctor Annual Salary:", tk.Entry(intern_add_window)),
            ("Hospital Name:", tk.Entry(intern_add_window)),
            ("Intern Year:", tk.Entry(intern_add_window)),
        ]

        # Use grid to organize labels and entries in two columns
        for i, (label, entry) in enumerate(label_entries):
            tk.Label(intern_add_window, text=label).grid(row=i * 2 + 1, column=0, padx=50, pady=10)
            entry.grid(row=i * 2 + 1, column=1, padx=20, pady=10)

        # Function to handle adding intern doctor details to the database
        def intern_GUI_db():
            try:
                values = [entry.get() for _, entry in label_entries]

                # Create a InternDoctor object
                new_doctor = InternDoctor(
                    doc_ID=values[0],
                    doc_name=values[1],
                    doc_gender=values[2],
                    doc_mobile=values[3],
                    doc_specialization=values[4],
                    doc_annualSal=values[5],
                    hospital_name=values[6],
                    intern_year=values[7]
                )

                new_doctor.insert_to_database()

                messagebox.showinfo("Success", "Doctor details added successfully!")

                # Close the window after adding details
                intern_add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")    
        tk.Button(intern_add_window, text="Add Intern Doctor", command=intern_GUI_db).grid(row=len(label_entries)*2, columnspan=2, pady=15)

    def add_senior_GUI(self):
        #Create a new window for adding Senior Doctor
        senior_add_window = tk.Toplevel(self.master)
        senior_add_window.title("Adding senior Doctor Details")
        senior_add_window.geometry("400x450")
        senior_add_window.configure(bg="#7FB3D5")
        tk.Label(senior_add_window, text="Please add Senior Doctor details", font=("Arial", 11), bg="#7FB3D5").grid(row=0, columnspan=2, pady=10)

        label_entries = [
            ("Doctor ID:", tk.Entry(senior_add_window)),
            ("Doctor Name:", tk.Entry(senior_add_window)),
            ("Doctor Gender:", tk.Entry(senior_add_window)),
            ("Doctor Mobile Number:", tk.Entry(senior_add_window)),
            ("Doctor Specialization:", tk.Entry(senior_add_window)),
            ("Doctor Annual Salary:", tk.Entry(senior_add_window)),
            ("Hospital Name:", tk.Entry(senior_add_window)),
            ("Retirement Year:", tk.Entry(senior_add_window)),
        ]

        # Use grid to organize labels and entries in two columns
        for i, (label, entry) in enumerate(label_entries):
            tk.Label(senior_add_window, text=label).grid(row=i * 2 + 1, column=0, padx=50, pady=10)
            entry.grid(row=i * 2 + 1, column=1, padx=20, pady=10)

        # Function to handle adding senior doctor details to the database
        def senior_GUI_db():
            try:
                values = [entry.get() for _, entry in label_entries]
                # Create a SeniorDoctor object
                new_doctor = SeniorDoctor(
                    doc_ID=values[0],
                    doc_name=values[1],
                    doc_gender=values[2],
                    doc_mobile=values[3],
                    doc_specialization=values[4],
                    doc_annualSal=values[5],
                    hospital_name=values[6],
                    retirement_year=values[7]
                )

                # Insert the doctor details into the database
                new_doctor.insert_to_database()

                messagebox.showinfo("Success", "Doctor details added successfully!")

                # Close the window after adding details
                senior_add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")    

        tk.Button(senior_add_window, text="Add Senior Doctor", command=senior_GUI_db).grid(row=len(label_entries)*2, columnspan=2, pady=15)

    def get_GUI(self):
        # Create a new window for getting doctor details
        get_window = tk.Toplevel(self.master)
        get_window.title("Get Doctor Details")
        get_window.geometry("300x200")
        get_window.configure(bg="#7FB3D5")
        self.label = tk.Label(get_window, text="Please enter DocID to retrieve information", font=("Arial", 11))
        self.label.pack(pady=20)

        tk.Label(get_window, text="Doctor ID:").pack(pady=10)
        doc_id_entry = tk.Entry(get_window)
        doc_id_entry.pack()

        # Function to handle getting doctor details from the database
        def get_GUI_db():
            try:
                doc_id_to_select = doc_id_entry.get()

                # Execute the SELECT query to retrieve doctor details
                cur.execute("SELECT * FROM doctor WHERE doc_ID = %s", (doc_id_to_select,))
                result = cur.fetchone()

                if result:
                    # Display doctor details in a messagebox
                    details_str = (
                        f"Doctor ID: {result[0]}\n"
                        f"\nDoctor Name: {result[1]}\n"
                        f"\nDoctor Gender: {result[2]}\n"
                        f"\nDoctor Mobile No: {result[3]}\n"
                        f"\nDoctor Specialization: {result[4]}\n"
                        f"\nDoctor Salary per year: {result[5]}\n"
                        f"\nHospital Name: {result[6]}\n"
                    )
                    if result[7] is not None:
                        details_str += f"\nIntern Year: {result[7]}\n"
                    if result[8] is not None:
                        details_str += f"\nRetirement Year: {result[8]}\n"

                    messagebox.showinfo("Doctor Information", details_str)
                else:
                    messagebox.showinfo("Doctor Information", "No record found.")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(get_window, text="Get Doctor", command=get_GUI_db).pack(pady=15)

    def update_GUI(self):
        # Create a new window for updating doctor details
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Doctor Details")
        update_window.geometry("400x500")
        update_window.configure(bg="#7FB3D5")
        self.label = tk.Label(update_window, text="Please enter updated information", font=("Arial", 11))
        self.label.pack(pady=20)

        # Entry fields for doctor details
        tk.Label(update_window, text="Doctor ID to Update:").pack(pady=10)
        doc_id_entry = tk.Entry(update_window)
        doc_id_entry.pack()

        tk.Label(update_window, text="New Name:").pack(pady=10)
        new_name_entry = tk.Entry(update_window)
        new_name_entry.pack()

        tk.Label(update_window, text="New Gender:").pack(pady=10)
        new_gender_entry = tk.Entry(update_window)
        new_gender_entry.pack()

        tk.Label(update_window, text="New Mobile Number:").pack(pady=10)
        new_mobile_entry = tk.Entry(update_window)
        new_mobile_entry.pack()

        tk.Label(update_window, text="New Specialization:").pack(pady=10)
        new_specialization_entry = tk.Entry(update_window)
        new_specialization_entry.pack()

        tk.Label(update_window, text="New Salary per Year:").pack(pady=10)
        new_annual_sal_entry = tk.Entry(update_window)
        new_annual_sal_entry.pack()

        # Function to handle updating doctor details in the database
        def update_GUI_db():
            try:
                # Get values from entry fields
                doc_id_to_update = doc_id_entry.get()
                new_name = new_name_entry.get()
                new_gender = new_gender_entry.get()
                new_mobile = new_mobile_entry.get()
                new_specialization = new_specialization_entry.get()
                new_annual_sal = new_annual_sal_entry.get()

                sql = "UPDATE doctor SET doc_name = %s, doc_gender = %s, doc_mobile = %s, doc_specialization = %s, doc_annualSal = %s WHERE doc_ID = %s"
                val = (new_name, new_gender, new_mobile, new_specialization, new_annual_sal, doc_id_to_update)

                # Execute the SQL update query
                cur.execute(sql, val)
                db.commit()
                messagebox.showinfo("Success", f"Doctor record with ID {doc_id_to_update} successfully updated!")

                # Close the update_window after updating details
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(update_window, text="Update Doctor", command=update_GUI_db).pack(pady=15)

    def delete_GUI(self):
        # Create a new window for deleting doctor details
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Doctor Details")
        delete_window.geometry("300x200")
        delete_window.configure(bg="#7FB3D5")
        self.label = tk.Label(delete_window, text="Please enter DocID to delete", font=("Arial", 11))
        self.label.pack(pady=20)

        # Entry field for doctor ID to delete
        tk.Label(delete_window, text="Doctor ID to Delete:").pack(pady=10)
        doc_id_entry = tk.Entry(delete_window)
        doc_id_entry.pack()

        # Function to handle deleting doctor details from the database
        def delete_GUI_db():
            try:
                doc_id_to_delete = doc_id_entry.get()

                # Create a AbstractDoctor object called 'delete' to delete a specific doctor's details
                delete = Doctor(doc_ID_to_delete=doc_id_to_delete)

                # Call the delete_from_database method of the Doctor object to initiate the deletion
                delete.delete_from_database()

                messagebox.showinfo("Success", f"Doctor record with ID {doc_id_to_delete} successfully deleted!")

                # Close the delete_window after deleting details
                delete_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(delete_window, text="Delete Doctor", command=delete_GUI_db).pack(pady=15)

    def close_connection_and_exit(self):
        # Close the database connection and exit the program
        cur.close()
        db.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = DocGUI(root)
    root.mainloop()  

