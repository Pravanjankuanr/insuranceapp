import tkinter as tk
from tkinter import messagebox
import requests

class DeletePartnerApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

        self.found_partner = None

        # ---------- Title ----------
        lbl_title = tk.Label(self, text="Delete Partner", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        self.create_widgets()

    def create_widgets(self):
        font_label = ('calibri', 15)
        font_entry = ('calibri', 15)

        form_frame = tk.Frame(self, padx=20, pady=20)
        form_frame.pack()

        tk.Label(form_frame, text="Partner Code / Name:", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entry_search = tk.Entry(form_frame, font=font_entry, width=25)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)

        self.result_label = tk.Label(form_frame, text="", font=('calibri', 12), fg="blue")
        self.result_label.grid(row=1, column=0, columnspan=2, pady=5)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Fetch", width=15, fg='#ffffff', bg='#007acc', font=('calibri', 12, 'bold'),
                  command=self.fetch_partner).grid(row=0, column=0, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete", width=15, fg='#ffffff', bg='#ff3300',
                                    font=('calibri', 12, 'bold'), command=self.delete_partner, state=tk.DISABLED)
        self.delete_btn.grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Clear", width=15, fg='#ffffff', bg='#999999', font=('calibri', 12, 'bold'),
                  command=self.clear_fields).grid(row=0, column=2, padx=5)

    def fetch_partner(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Validation Error", "Please enter a partner code or name.")
            return

        try:
            response = requests.get("http://127.0.0.1:5000/get_cp/search", params={"query": keyword})
            data = response.json()

            if data.get("success") and data.get("partners"):
                partner = data["partners"][0]
                self.found_partner = partner
                self.result_label.config(
                    text=f"Partner Found: {partner['cp_name']} ({partner['cp_code']})", fg="green"
                )
                self.delete_btn.config(state=tk.NORMAL)
            else:
                self.result_label.config(text="No partner found.", fg="red")
                messagebox.showinfo("No Results", data.get("message", "No matching partners found."))
                self.found_partner = None
                self.delete_btn.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to connect to server:\n{e}")

    def delete_partner(self):
        if not self.found_partner:
            messagebox.showwarning("No Selection", "Please fetch a partner to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete partner: {self.found_partner['cp_code']}?")
        if not confirm:
            return

        try:
            cp_code = self.found_partner['cp_code']
            response = requests.delete(f"http://127.0.0.1:5000/delete_cp/{cp_code}")
            data = response.json()

            if response.status_code == 200:
                messagebox.showinfo("Deleted", data.get("message"))
                self.clear_fields()
            else:
                messagebox.showwarning("Failed", data.get("message"))
        except Exception as e:
            messagebox.showerror("Server Error", f"Error deleting partner:\n{e}")

    def clear_fields(self):
        self.entry_search.delete(0, tk.END)
        self.result_label.config(text="")
        self.found_partner = None
        self.delete_btn.config(state=tk.DISABLED)