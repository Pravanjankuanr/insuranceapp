import tkinter as tk
from tkinter import messagebox
import requests

class DeleteCustomerApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(bg="#d9e6fc")

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Delete Customer", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        # 🔍 Search fields
        tk.Label(self, text="Enter Code / Name / PAN", font=("Cambria", 12), bg="#d9e6fc").pack()
        self.search_entry = tk.Entry(self, font=("Cambria", 12))
        self.search_entry.pack(pady=5)

        tk.Button(self, text="Search", font=("Cambria", 12), bg="blue", fg="white",
                  command=self.search_customer).pack(pady=10)

        self.result_text = tk.Text(self, height=6, font=("Cambria", 12), state="disabled")
        self.result_text.pack(pady=10)

        tk.Button(self, text="Delete Customer", font=("Cambria", 12), bg="red", fg="white",
                  command=self.delete_customer).pack(pady=5)

    def search_customer(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter code, name, or PAN.")
            return

        try:
            response = requests.get(f"https://insuranceapp-6kjz.onrender.com/get_customer", params={"query": query})
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                customer = data["data"]
                self.show_customer(customer)
                self.found_customer_id = customer["cust_id"]  # store ID for delete
            else:
                messagebox.showinfo("Not Found", data.get("message", "Customer not found."))
                self.clear_customer()
        except Exception as e:
            messagebox.showerror("Server Error", str(e))

    def show_customer(self, customer):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        details = f"Code: {customer['cust_id']}\nName: {customer['cust_name']}\nPAN: {customer['pan']}"
        self.result_text.insert("end", details)
        self.result_text.config(state="disabled")

    def clear_customer(self):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        self.result_text.config(state="disabled")
        self.found_customer_id = None

    def delete_customer(self):
        if not hasattr(self, 'found_customer_id') or not self.found_customer_id:
            messagebox.showwarning("No Customer", "Please search and select a customer first.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?")
        if not confirm:
            return

        try:
            response = requests.delete(
                "https://insuranceapp-6kjz.onrender.com/delete_customer",
                json={"query": self.found_customer_id}
            )

            try:
                result = response.json()
            except ValueError:
                messagebox.showerror("Server Error", "Invalid response from server.")
                return

            if response.status_code == 200 and result.get("success"):
                messagebox.showinfo("Deleted", "Customer deleted successfully.")
                self.clear_customer()
                self.search_entry.delete(0, tk.END)
                self.found_customer_id = None
            else:
                messagebox.showerror("Failed", result.get("message", "Could not delete."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not reach server:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DeleteCustomerApp(root)
    root.mainloop()