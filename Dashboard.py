import tkinter as tk
from tkinter import ttk
from Testfordb import *  #Delete this line, and import you own code
from GUI_DOC import *

#The main GUI
class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.instance = None

        self.title("Dashboard Clinic")

        # Frame untuk menu di sebelah kiri
        self.menu_frame = tk.LabelFrame(self, width=200, height=300, relief="ridge", padx=20, pady=10, bg="lightblue")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Tambahkan beberapa widget ke dalam menu
        self.menu_label = ttk.Label(self.menu_frame, text="Menu", font=("Arial", 20))
        self.menu_label.pack(pady=30)
        
        self.doctor_btn = ttk.Button(self.menu_frame, text="Doctor", command=self.on_doctor)
        self.doctor_btn.pack(pady=10)

        self.patient_btn = ttk.Button(self.menu_frame, text="Patient", command=self.on_patient)
        self.patient_btn.pack(pady=10)

        self.appointment_btn = ttk.Button(self.menu_frame, text="Appointment", command=self.on_appointment)
        self.appointment_btn.pack(pady=10)

        self.prescription_btn = ttk.Button(self.menu_frame, text="Prescription", command=self.on_prescription)
        self.prescription_btn.pack(pady=10)

        self.shop_btn = ttk.Button(self.menu_frame, text="Shop", command=self.on_shop)
        self.shop_btn.pack(pady=10)

        self.exit_btn = ttk.Button(self.menu_frame, text="Exit", command=self.destroy)
        self.exit_btn.pack(pady=10)

    def no_repeat(self, cls):
        if not self.instance:
            self.instance = cls(self)

#Calling your code here 
    def on_doctor(self):
        print("Tombol doctor diklik")
        # doctor_gui = DocGUI(self)
        self.no_repeat(DocGUI)
        
    def on_patient (self):
        print("Tombol patient diklik")

    def on_appointment (self):
        print("Tombol appointment diklik")

    def on_prescription(self):
        print("Tombol prescription diklik")
        self.no_repeat(PrescriptionApp)

    def on_shop(self):
        print("Tombol shop diklik") 

if __name__ == "__main__":
    app = Dashboard()
    app.geometry("500x400")
    app.mainloop()