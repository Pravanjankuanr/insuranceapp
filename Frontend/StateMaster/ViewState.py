import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ViewStateApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(bg="#d9e6fc")

        #Title
        lbl_title = tk.Label(self, text="Delete State", fg='black',bg="#d9e6fc",
                             font=('cambria', 20, 'bold'), padx=10, pady=10)
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        # Search Frame
        search_frame = tk.Frame(self, bg="#d9e6fc")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search (Code or Name):", bg="#d9e6fc", font=("Cambria", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_state).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="View All", command=self.view_all_states).pack(side=tk.LEFT, padx=5)


# === Treeview Style ===
        style = ttk.Style()
        style.configure("State.Treeview",
                        font=("Cambria", 12),
                        rowheight=30,
                        background="#d9e6fc",
                        foreground="black",
                        fieldbackground="white")
        style.map('State.Treeview', background=[('selected', '#a3c9f1')])

        style.configure("State.Treeview.Heading", font=("Cambria", 13, "bold"))

        # === Table Frame ===
        tree_frame = tk.Frame(self, width=500, height=350, bg="#d9e6fc")
        tree_frame.pack(pady=20)
        tree_frame.pack_propagate(False)

        # === Scrollbars ===
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        y_scroll.pack(side=tk.RIGHT, fill="y")

        # === Treeview Widget ===
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Code", "Name"),
            show="headings",
            yscrollcommand=y_scroll.set,
            style="State.Treeview"
        )
        y_scroll.config(command=self.tree.yview)


        self.tree.heading("Code", text="State Code")
        self.tree.heading("Name", text="State Name")

        self.tree.column("Code", anchor="center", width=250)
        self.tree.column("Name", anchor="center", width=250)

        self.tree.pack(fill="both", expand=True)
        
    def search_state(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("Input Needed", "Please enter a state code or name.")
            return
        self.fetch_states({"search": keyword})

    def view_all_states(self):
        self.fetch_states()

    def fetch_states(self, params=None):
        try:
            url = "http://127.0.0.1:5000/get_state/search" if params else "http://127.0.0.1:5000/get_state"
            response = requests.get(url, params={"query": params["search"]} if params else None)

            res = response.json()
            self.tree.delete(*self.tree.get_children())
            if res.get("success"):
                for state in res["states"]:
                    self.tree.insert("", "end", values=(state["state_Code"], state["state_Name"]))
            else:
                messagebox.showinfo("No Data", res.get("message", "No matching state found."))
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

# --------- Standalone Run ---------
if __name__ == "__main__":
    root = tk.Tk()
    app = ViewStateApp(root)  # Can be run standalone with no home page
    root.mainloop()