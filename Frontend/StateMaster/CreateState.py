import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import openpyxl
import csv
import requests

class CreateStateApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Create State", fg='black',bg="#d9e6fc",
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

        tk.Label(form_frame, text="State Code:",bg="#d9e6fc", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_code = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_code.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="State Name:",bg="#d9e6fc", font=font_label).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_name = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self, bg="#d9e6fc")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save", width=20, height=1, fg='white', bg='#ff3300',
                  font=('calibri', 12, 'bold'), command=self.save_state).grid(row=0, column=0, padx=3, pady=5)
        tk.Button(btn_frame, text="Upload Excel/CSV", width=20, height=1, fg='white', bg='#ff3300',
                  font=('calibri', 12, 'bold'), command=self.import_excel_or_csv).grid(row=0, column=4, padx=3, pady=5)
        tk.Button(btn_frame, text="Clear", width=20, height=1, fg='white', bg='#ff3300',
                  font=('calibri', 12, 'bold'), command=self.clear_fields).grid(row=0, column=3, padx=3, pady=5)
        
    def save_state(self):
        name = self.entry_name.get().strip().title()
        code = self.entry_code.get().strip().upper()
        if not name or not code:
            messagebox.showwarning("Validation Error", "Both fields are required.")
            return

        try:
            response = requests.post("http://127.0.0.1:5000/add_state", json={
                "state_Code": code,
                "state_Name": name
            })

            res = response.json()
            if res.get("success"):
                messagebox.showinfo("Success", res.get("message"))
                self.clear_fields()
            else:
                messagebox.showwarning("Failed", res.get("message"))
        except Exception as e:
            messagebox.showerror("Error", f"Request failed: {e}")


    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)

    def import_excel_or_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Excel and CSV files", "*.xlsx *.csv"),
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv")
        ])
        
        if not file_path:
            return

        data = []

        try:
            if file_path.endswith(".xlsx"):
                # Handle Excel
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    code, name = row
                    if code and name:
                        data.append({
                            "state_Code": str(code).strip().upper(),
                            "state_Name": str(name).strip().title()
                        })

            elif file_path.endswith(".csv"):
                # Handle CSV
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    for row in reader:
                        if len(row) < 2:
                            continue
                        code, name = row[0], row[1]
                        if code and name:
                            data.append({
                                "state_Code": code.strip().upper(),
                                "state_Name": name.strip().title()
                            })

            else:
                messagebox.showerror("Unsupported File", "Please select a .csv or .xlsx file only.")
                return

            if not data:
                messagebox.showwarning("No Data", "No valid data found in the file.")
                return

            # Send to Flask API
            response = requests.post("http://127.0.0.1:5000/bulk_add_state", json=data)
            res = response.json()

            if res.get("success"):
                messagebox.showinfo("Import Result", f"{res['inserted']} state saved successfully, Duplicate Entry: {res['skipped']}")
            else:
                messagebox.showerror("Error", res.get("message"))

        except Exception as e:
            messagebox.showerror("Error", f"File import failed: {str(e)}")