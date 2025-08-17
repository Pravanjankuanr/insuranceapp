import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardApp(tk.Frame):
    def __init__(self, parent, home_page=None):
        super().__init__(parent)
        self.parent = parent
        self.home_page = home_page
        
        # ---------- Header ----------
        tk.Label(self, text="Dashboard", font=("Cambria", 20, "bold"),
                  fg="black", pady=20).pack(fill=tk.X)

        # ---------- Info Boxes ----------
        self.metrics_frame = tk.Frame(self, bg="#ffffff")
        self.metrics_frame.pack(pady=20)

        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        font_label = ('calibri', 15)
        font_entry = ('calibri', 18)


        self.labels = {}
        for i, label in enumerate(["Total Employees", "Total Customers", "Channel Partners", "Branches", "State"]):
            frame = tk.Frame(self.metrics_frame, bg="#ecf0f1", padx=30, pady=20, bd=1, relief="ridge")
            frame.grid(row=0, column=i, padx=10)
            tk.Label(frame, text=label, font=font_label, bg="#ecf0f1").pack()
            value_lbl = tk.Label(frame, text="0", font=font_entry, bg="#ecf0f1", fg="#1f4e79")
            value_lbl.pack()
            self.labels[label] = value_lbl

        # ---------- Chart Area ----------
        self.chart_frame = tk.Frame(self, bg="#ffffff")
        self.chart_frame.pack(pady=20, fill="both", expand=True)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", font=("Calibri", 14),
                  bg="#1f618d", fg="white", command=self.load_data).pack(side="left", padx=10)

         # Load data initially
        self.load_data()

    def load_data(self):
        """Fetch metrics and chart data from MySQL."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="@Raja12",
                database="lidata"
            )
            cursor = conn.cursor()

            # Total Counts
            cursor.execute("SELECT COUNT(*) FROM employee")
            self.labels["Total Employees"].config(text=cursor.fetchone()[0])

            cursor.execute("SELECT COUNT(*) FROM customer")
            self.labels["Total Customers"].config(text=cursor.fetchone()[0])

            cursor.execute("SELECT COUNT(*) FROM cp")
            self.labels["Channel Partners"].config(text=cursor.fetchone()[0])

            cursor.execute("SELECT COUNT(*) FROM branch")
            self.labels["Branches"].config(text=cursor.fetchone()[0])

            # # Month-wise policy logs
            # cursor.execute("""
            #     SELECT MONTH(entry_date), COUNT(*) 
            #     FROM proposal 
            #     WHERE entry_date IS NOT NULL
            #     GROUP BY MONTH(entry_date)
            #     ORDER BY MONTH(entry_date)
            # """)
            # month_data = cursor.fetchall()

            cursor.close()
            conn.close()

            # self.plot_chart(month_data)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load data:\n{err}")

    def plot_chart(self, month_data):
        """Draw bar chart for month-wise policy logs."""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        x = [months[m - 1] for m, _ in month_data]
        y = [count for _, count in month_data]

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        ax.bar(x, y, color="#3498db")
        ax.set_title("Month-wise Policy Logging")
        ax.set_ylabel("Policy Count")
        ax.set_xlabel("Month")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------- Standalone test ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()