import tkinter as tk
from tkinter import messagebox
import requests

class UpdateCustomerApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Update Customer", fg='black',bg="#d9e6fc",
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
            tk.Label(self.form_frame, text=label + ":", bg="#d9e6fc", font=("Calibri", 12)).grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self.form_frame, font=("Calibri", 12), width=30)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            if label == "Customer ID":
                entry.config(state="readonly")
            self.entries[label] = entry

        tk.Button(self, text="Update Customer", command=self.update_customer, bg="green", fg="white", font=("Calibri", 12)).pack(pady=10)

    def fetch_customer(self):
        query = self.search_query.get().strip()
        if not query:
            messagebox.showerror("Error", "Enter Customer ID / Name / PAN to search.")
            return

        try:
            # CHANGED: use GET instead of POST
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
                    "DOB" : "dob",
                    "Email": "email",
                    "PAN": "pan",
                    "Address":"address",
                    "State Code": "state_code",
                    "State Name": "state_name"
                }

                for key in self.entries:
                    entry = self.entries[key]
                    entry.config(state="normal")
                    entry.delete(0, tk.END)
                    db_key = key_map.get(key, key.lower().replace(" ", "_"))
                    entry.insert(0, customer.get(db_key, ""))
                    if key == "Customer ID":
                        entry.config(state="readonly")

                # Store the customer ID to reuse in deletion
                self.found_customer_id = customer.get("cust_id")

            else:
                messagebox.showinfo("Not Found", data.get("message", "Customer not found."))
                for entry in self.entries.values():
                    entry.config(state="normal")
                    entry.delete(0, tk.END)
                self.entries["Customer ID"].config(state="readonly")
                self.found_customer_id = None

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server Error", f"Could not reach server:\n{e}")

    def update_customer(self):
        data = {
            "cust_id": self.entries["Customer ID"].get().strip(),
            "cust_name": self.entries["Customer Name"].get().strip(),
            "mob_number": self.entries["Mobile"].get().strip(),
            "dob": self.entries["DOB"].get().strip(),
            "pan": self.entries["PAN"].get().strip(),
            "email": self.entries["Email"].get().strip(),
            "address": self.entries["Address"].get().strip(),
            "state_code": self.entries["State Code"].get().strip(),
            "state_name": self.entries["State Name"].get().strip()
        }

        if not data["cust_id"]:
            messagebox.showerror("Error", "Please search and select a customer first.")
            return

        try:
            response = requests.put("http://127.0.0.1:5000/update_customer", json=data)
            result = response.json()

            if response.status_code == 200 and result.get("success"):
                messagebox.showinfo("Success", result.get("message", "Customer updated successfully."))
            else:
                messagebox.showerror("Update Failed", result.get("message", "Could not update customer."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server Error", f"Could not reach server:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateCustomerApp(root)
    root.mainloop()