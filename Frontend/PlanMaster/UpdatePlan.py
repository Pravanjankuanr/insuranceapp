import tkinter as tk
from tkinter import messagebox
import requests

class UpdatePlanApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Update Plan", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        self.create_widgets()

    def create_widgets(self):
        font_label = ('calibri', 15)
        font_entry = ('calibri', 15)

        form_frame = tk.Frame(self, padx=20, pady=20, bg="#d9e6fc")
        form_frame.pack()

        # --- Search Field ---
        tk.Label(form_frame, text="Plan Code / Name:", font=font_label).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_search = tk.Entry(form_frame, font=font_entry)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Fetch", width=12, bg="#007acc", fg="white",
                  font=('calibri', 12, 'bold'), command=self.fetch_plan).grid(row=0, column=2, padx=10)

        # Add result label
        self.result_label = tk.Label(form_frame, text="", font=("calibri", 12), fg="green")
        self.result_label.grid(row=1, column=0, columnspan=3, pady=(5, 15))

        # --- Editable Fields ---
        tk.Label(form_frame, text="Plan Code:", font=font_label).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_code = tk.Entry(form_frame, font=font_entry, state= 'readonly')
        self.entry_code.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Plan Name:", font=font_label).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame, font=font_entry)
        self.entry_name.grid(row=3, column=1, padx=5, pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(self , bg="#d9e6fc")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Update", width=15, bg="#28a745", fg="white",
                  font=('calibri', 12, 'bold'), command=self.update_plan).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Clear", width=15, bg="#6c757d", fg="white",
                  font=('calibri', 12, 'bold'), command=self.clear_fields).grid(row=0, column=1, padx=10)

    def fetch_plan(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Validation Error", "Please enter a plan code or name.")
            return

        try:
            response = requests.get("http://127.0.0.1:5000/get_plan/search", params={"query": keyword})
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                plans = data["plans"]
                if len(plans) == 1:
                    plan = plans[0]
                    self.result_label.config(text=f"Found: {plan['plan_code']} - {plan['plan_name']}")

                    # Insert into readonly Entry
                    self.entry_code.config(state='normal')
                    self.entry_code.delete(0, tk.END)
                    self.entry_code.insert(0, plan['plan_code'])
                    self.entry_code.config(state='readonly')

                    self.entry_name.delete(0, tk.END)
                    self.entry_name.insert(0, plan['plan_name'])

                    self.original_code = plan['plan_code']
                elif len(plans) > 1:
                    self.result_label.config(text="Multiple plans found. Please enter full code.")
                    messagebox.showinfo("Multiple Matches", "More than one match found. Please refine your search.")
                else:
                    self.result_label.config(text="No plan found.")
                    messagebox.showinfo("No Match", "No matching plan found.")
            else:
                self.result_label.config(text="Search failed.")
                messagebox.showwarning("Error", data.get("message", "Something went wrong."))
        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to connect to server:\n{e}")

    def update_plan(self):
        updated_code = self.entry_code.get().strip()
        updated_name = self.entry_name.get().strip()

        if not hasattr(self, 'original_code'):
            messagebox.showwarning("Validation Error", "Please fetch a plan before updating.")
            return

        if not updated_code or not updated_name:
            messagebox.showwarning("Validation Error", "Please fill all fields.")
            return

        try:
            response = requests.put(f"http://127.0.0.1:5000/update_plan/{self.original_code}", json={
                            "plan_name": updated_name})

            data = response.json()
            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Success", data.get("message"))
                self.clear_fields()
            else:
                messagebox.showwarning("Update Failed", data.get("message"))
        except Exception as e:
            messagebox.showerror("Server Error", f"Update failed:\n{e}")

    def clear_fields(self):
        self.entry_search.delete(0, tk.END)

        # Temporarily make plan code editable to clear it
        self.entry_code.config(state='normal')
        self.entry_code.delete(0, tk.END)
        self.entry_code.config(state='readonly')

        self.entry_name.delete(0, tk.END)
        self.result_label.config(text="")

        if hasattr(self, 'original_code'):
            del self.original_code
