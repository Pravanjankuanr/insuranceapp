import tkinter as tk
import requests
from tkinter import messagebox
from HomePage import HomePage

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Safora")
        self.state('zoomed')
        self.configure(bg="#d9e6fc")

        tk.Label(self, text="Login ID", font=("Cambria", 12), bg="#d9e6fc").pack(pady=(30, 5))
        self.login_id = tk.Entry(self, font=("Cambria", 12))
        self.login_id.pack(pady=5)

        tk.Label(self, text="Password", font=("Cambria", 12), bg="#d9e6fc").pack(pady=5)
        self.password = tk.Entry(self, font=("Cambria", 12), show="*")
        self.password.pack(pady=5)

        tk.Button(self, text="Login", command=self.validate_login, bg="#1f4e7a", fg="white", font=("Cambria", 12)).pack(pady=20)
        tk.Button(self, text="Forgot Password?", command=self.forgot_password, font=("Cambria", 10), bg="#d9e6fc", bd=0, fg="blue").pack()

    def validate_login(self):
        user = self.login_id.get().strip()
        password = self.password.get().strip()

        try:
            response = requests.post("http://127.0.0.1:5000/login", json={
                "username": user,
                "password": password
            })

            if response.status_code == 200 and response.json().get("success"):
                self.destroy()
                home = HomePage()
                home.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid User ID or Password")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Server error: {e}")

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Contact admin to reset password.")

if __name__ == "__main__":
    login = LoginPage()
    login.mainloop()