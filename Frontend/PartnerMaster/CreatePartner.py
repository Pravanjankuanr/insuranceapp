import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import openpyxl
import csv
import requests
import os

class CreatePartnerApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Create Partner", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Form Frame ----------
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        font_label = ('calibri', 15)
        font_entry = ('calibri', 15)        
        
        form_frame = tk.Frame(self, padx=20, pady=20)
        form_frame.pack()

        tk.Label(form_frame, text="Channel Partner Code:", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_code = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_code.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Channel Partner Name:", font=font_label).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_name = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.save_cp).grid(row=0, column=0, padx=3, pady=5)
        tk.Button(btn_frame, text="Import Excel / CSV", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.import_file).grid(row=0, column=1, padx=3, pady=5)
        tk.Button(btn_frame, text="Clear", width=20, height = 1, fg='#dddddd', bg='#ff3300', font=('calibri', 12, 'bold'), command=self.clear_fields).grid(row=0, column=2, padx=3, pady=5)

    def save_cp(self):
        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        
        if not name or not code:
            messagebox.showwarning("Validation Error", "Both fields are required.")
            return

        url = "http://127.0.0.1:5000/add_partner"  # Replace with your hosted Flask server IP
        payload = {"cp_code": code, "cp_name": name}

        try:
            response = requests.post(url, json=payload)
            result = response.json()

            if response.status_code == 201:
                messagebox.showinfo("Success", result.get("message", "Saved successfully."))
                self.clear_fields()
            else:
                messagebox.showwarning("Failed", result.get("message", "Could not save."))
        except Exception as e:
            messagebox.showerror("Error", f"API call failed: {str(e)}")

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Excel and CSV files", "*.xlsx *.csv"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx")
        ])
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()

        partner_data = []

        try:
            if ext == ".csv":
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            partner_data.append({
                                "cp_code": row[0].strip(),
                                "cp_name": row[1].strip()
                            })

            elif ext == ".xlsx":
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    code, name = row
                    if code and name:
                        partner_data.append({
                            "cp_code": str(code).strip(),
                            "cp_name": str(name).strip()
                        })
            else:
                messagebox.showerror("Invalid File", "Please select a valid .csv or .xlsx file.")
                return

            if not partner_data:
                messagebox.showwarning("No Data", "No valid channel partner data found.")
                return

            # ---------- Send to API ----------
            url = "http://127.0.0.1:5000/bulk_add_cp"  # Replace with your actual server URL
            response = requests.post(url, json={"partners": partner_data})

            if response.status_code == 200:
                result = response.json()
                messagebox.showinfo("Import Result", f"Inserted: {result.get('inserted', 0)}, Skipped: {result.get('skipped', 0)}")
            else:
                messagebox.showerror("Import Failed", response.json().get("message", "Failed to import data."))

        except Exception as e:
            messagebox.showerror("Error", f"File import failed: {str(e)}")