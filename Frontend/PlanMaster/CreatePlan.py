import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import openpyxl
import csv
import requests

class CreatePlanApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Create Plan", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Form Frame ----------
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        font_label = ('calibri', 15)
        font_entry = ('calibri', 15)
        
        form_frame = tk.Frame(self, padx=20, pady=20, bg="#d9e6fc")
        form_frame.pack()

        tk.Label(form_frame, text="Plan Code:",bg="#d9e6fc", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_code = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_code.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Plan Name:", bg="#d9e6fc", font=font_label).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_name = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self, bg="#d9e6fc")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.save_plan).grid(row=0, column=0, padx=3, pady=5)
        tk.Button(btn_frame, text="Upload Excel / CSV", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.import_excel).grid(row=0, column=4, padx=3, pady=5)
        tk.Button(btn_frame, text="Clear", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.clear_fields).grid(row=0, column=3, padx=3, pady=5)
            

    def save_plan(self):
        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        if not name or not code:
            messagebox.showwarning("Validation Error", "Both fields are required.")
            return

        try:
            response = requests.post("http://127.0.0.1:5000/add_plan", json={
                "plan_code": code,
                "plan_name": name
            })
            data = response.json()
            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Success", data.get("message"))
                self.clear_fields()
            else:
                messagebox.showwarning("Error", data.get("message"))
        except Exception as e:
            messagebox.showerror("Server Error", f"Error connecting to server:\n{e}")



    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)

    def import_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel/CSV files", "*.xlsx *.csv"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        plan_data = []

        try:
            if file_path.endswith(".xlsx"):
                # Handle Excel file
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    code, name = row
                    if code and name:
                        plan_data.append({"plan_code": str(code), "plan_name": str(name)})

            elif file_path.endswith(".csv"):
                # Handle CSV file
                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # Skip header row
                    for row in reader:
                        if len(row) >= 2:
                            code, name = row[0].strip(), row[1].strip()
                            if code and name:
                                plan_data.append({"plan_code": code, "plan_name": name})

            else:
                messagebox.showwarning("Invalid File", "Unsupported file format.")
                return

            if not plan_data:
                messagebox.showwarning("No Data", "No valid rows found in file.")
                return

            response = requests.post("http://127.0.0.1:5000/bulk_add_plan", json={"plans": plan_data})
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Import Result", data.get("message"))
            else:
                messagebox.showwarning("Import Failed", data.get("message"))

        except Exception as e:
            messagebox.showerror("Import Error", f"Error reading file or connecting to server:\n{e}")