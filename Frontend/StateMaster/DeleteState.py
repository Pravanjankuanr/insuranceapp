import tkinter as tk
from tkinter import messagebox
import requests

class DeleteStateApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        self.configure(bg="#d9e6fc")

                # ---------- Title ----------
        lbl_title = tk.Label(self, text="Delete State", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        form_frame = tk.Frame(self, bg="#d9e6fc")
        form_frame.pack()

        tk.Label(form_frame, text="Enter State Code or Name:",bg="#d9e6fc", 
                 font=("calibri", 14)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_search = tk.Entry(form_frame, font=("calibri", 14), width=30)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(form_frame, text="Search", font=("calibri", 12, "bold"),
                  bg="#007acc", fg="white", command=self.search_state).grid(row=0, column=2, padx=10)

        self.result_label = tk.Label(self, text="", font=("calibri", 14), bg="#d9e6fc")
        self.result_label.pack(pady=10)

        self.delete_btn = tk.Button(self, text="Delete State", font=("calibri", 12, "bold"),
                                    bg="red", fg="white", command=self.delete_state)
        self.delete_btn.pack(pady=10)
        self.delete_btn.config(state=tk.DISABLED)

        self.found_state_code = None  # Store searched code for deletion

    def search_state(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a state code or name.")
            return

        try:
            response = requests.get("http://127.0.0.1:5000/get_state/search", params={"query": keyword})
            res = response.json()

            if res.get("success") and res.get("states"):
                state = res["states"][0]
                self.found_state_code = state["state_Code"]
                self.result_label.config(
                    text=f"State Found: {state['state_Name']} ({state['state_Code']})", fg="green"
                )
                self.delete_btn.config(state=tk.NORMAL)
            else:
                self.result_label.config(text="State not found.", fg="red")
                self.delete_btn.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search state:\n{str(e)}")

    def delete_state(self):
        if not self.found_state_code:
            messagebox.showwarning("No State", "No valid state selected to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{self.found_state_code}'?")
        if not confirm:
            return

        try:
            response = requests.delete("http://127.0.0.1:5000/delete_state", params={"code": self.found_state_code})
            res = response.json()

            if res.get("success"):
                messagebox.showinfo("Success", res.get("message"))
                self.result_label.config(text="")
                self.entry_search.delete(0, tk.END)
                self.delete_btn.config(state=tk.DISABLED)
                self.found_state_code = None
            else:
                messagebox.showwarning("Failed", res.get("message"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete state:\n{str(e)}")
