import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import csv
import json
from openpyxl import Workbook

class ReportApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        tk.Label(self, text="Export Report", font=('Cambria', 20, 'bold')).pack(pady=10)

        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # Dropdowns
        tk.Label(control_frame, text="Data Type:", font=("Calibri", 12)).grid(row=0, column=0, padx=5)
        self.data_type = ttk.Combobox(control_frame, values=["Customer", "State", "Partner"], state="readonly")
        self.data_type.grid(row=0, column=1, padx=5)
        self.data_type.current(0)

        tk.Label(control_frame, text="Export Format:", font=("Calibri", 12)).grid(row=0, column=2, padx=5)
        self.export_format = ttk.Combobox(control_frame, values=["CSV", "Excel", "TXT", "JSON"], state="readonly")
        self.export_format.grid(row=0, column=3, padx=5)
        self.export_format.current(0)

        # Export Button
        tk.Button(self, text="Export", font=("Calibri", 12, "bold"),
                  bg="#4CAF50", fg="white", width=20,
                  command=self.export_data).pack(pady=10)

    def fetch_data_from_server(self, data_type):
        endpoints = {
            "Customer": "http://localhost:5000/get_all_customers",
            "State": "http://localhost:5000/get_state",
            "Partner": "http://localhost:5000/get_all_cp"
        }

        try:
            response = requests.get(endpoints[data_type])
            if response.status_code == 200 and response.json().get("success"):
                if data_type == "Customer":
                    return response.json()["data"]
                elif data_type == "State":
                    return response.json()["states"]
                elif data_type == "Partner":
                    return response.json()["partners"]
            else:
                raise Exception(response.json().get("message", "Unknown error"))
        except Exception as e:
            messagebox.showerror("Fetch Error", f"Failed to fetch data: {e}")
            return None


    def export_data(self):
        data_type = self.data_type.get()
        export_format = self.export_format.get()
        data = self.fetch_data_from_server(data_type)
        if not data:
            return

        filetypes = {
            "CSV": ("CSV files", "*.csv"),
            "Excel": ("Excel files", "*.xlsx"),
            "TXT": ("Text files", "*.txt"),
            "JSON": ("JSON files", "*.json")
        }

        file_ext = filetypes[export_format][1].replace("*", "")
        file_path = filedialog.asksaveasfilename(defaultextension=file_ext, filetypes=[filetypes[export_format]])
        if not file_path:
            return

        try:
            headers = list(data[0].keys()) if data else []

            if export_format == "CSV":
                with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)

            elif export_format == "Excel":
                wb = Workbook()
                ws = wb.active
                ws.append(headers)
                for row in data:
                    ws.append([row[col] for col in headers])
                wb.save(file_path)

            elif export_format == "TXT":
                with open(file_path, mode='w', encoding='utf-8') as f:
                    for row in data:
                        line = ', '.join(f"{k}: {v}" for k, v in row.items())
                        f.write(line + "\n")

            elif export_format == "JSON":
                with open(file_path, mode='w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {e}")