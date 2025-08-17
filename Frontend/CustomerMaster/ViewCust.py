import tkinter as tk
from tkinter import messagebox
import requests

class ViewCustomerApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="View Customer", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        self.search_query = tk.Entry(self, font=("Calibri", 14), width=30)
        self.search_query.pack(pady=5)
        tk.Button(self, text="Search", command=self.fetch_customer, bg="blue", fg="white", font=("Calibri", 12)).pack(pady=5)

        self.form_frame = tk.Frame(self, bg="#d9e6fc")
        self.form_frame.pack(pady=10)

        labels = ["Customer ID", "Customer Name", "Mobile", "DOB", "Email", "PAN", "Address", "State Code", "State Name"]
        self.entries = {}

        for idx, label in enumerate(labels):
            tk.Label(self.form_frame, text=label + ":",bg="#d9e6fc", font=("Calibri", 12)).grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self.form_frame, font=("Calibri", 12), width=30, state="readonly")
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[label] = entry

    def fetch_customer(self):
        query = self.search_query.get().strip()
        if not query:
            messagebox.showerror("Error", "Enter Customer ID / Name / PAN to search.")
            return

        try:
            response = requests.get("http://127.0.0.1:5000/get_customer", params={"query": query})
            try:
                data = response.json()
            except ValueError:
                messagebox.showerror("Server Error", "Invalid response from server.")
                return

            if response.status_code == 200 and data.get("success"):
                customer = data.get("data", {})

                key_map = {
                    "Customer ID": "cust_id",
                    "Customer Name": "cust_name",
                    "Mobile": "mob_number",
                    "DOB": "dob",
                    "Email": "email",
                    "PAN": "pan",
                    "Address": "address",
                    "State Code": "state_code",
                    "State Name": "state_name"
                }

                for key in self.entries:
                    entry = self.entries[key]
                    entry.config(state="normal")
                    db_key = key_map.get(key, key.lower().replace(" ", "_"))
                    entry.delete(0, tk.END)
                    entry.insert(0, customer.get(db_key, ""))
                    entry.config(state="readonly")

            else:
                messagebox.showinfo("Not Found", data.get("message", "Customer not found."))
                for entry in self.entries.values():
                    entry.config(state="normal")
                    entry.delete(0, tk.END)
                    entry.config(state="readonly")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server Error", f"Could not reach server:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("View Customer")
    app = ViewCustomerApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()