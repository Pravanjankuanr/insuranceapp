# import win32event
# import win32api
# import winerror
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


# mutex = win32event.CreateMutex(None, False, "my_unique_app_mutex_name")

# # If mutex already exists, another instance is running
# if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
#     print("already running.")
#     sys.exit(0)

# Replace these with your actual modules
from CustomerMaster.CreateCust import CustomerApp
from CustomerMaster.DeleteCust import DeleteCustomerApp
from CustomerMaster.UpdateCust import UpdateCustomerApp
from CustomerMaster.ViewCust import ViewCustomerApp
from PlanMaster.CreatePlan import CreatePlanApp
from PlanMaster.DeletePlan import DeletePlanApp
from PlanMaster.UpdatePlan import UpdatePlanApp
from PlanMaster.ViewPlan import ViewPlanApp
from PartnerMaster.CreatePartner import CreatePartnerApp
from PartnerMaster.DeletePartner import DeletePartnerApp
from PartnerMaster.UpdatePartner import UpdatePartnerApp
from PartnerMaster.ViewPartner import ViewPartnerApp
from StateMaster.CreateState import CreateStateApp
from StateMaster.DeleteState import DeleteStateApp
from StateMaster.ViewState import ViewStateApp
from ProposalMaster.Proposal import ProposalApp
from EmployeeMaster.Employee import EmployeeApp
from ReportMaster.Dashboard import DashboardApp
from ReportMaster.Report import ReportApp
from BranchMaster.CreateBranch import CreateBranchApp

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Safora Life insurance")
        self.state('zoomed')  # For Windows OS
        self.configure(bg="#a1bff7")

        # Header Frame
        header_frame = tk.Frame(self, bg="#1f4e7a")
        header_frame.pack(fill="x")

        # Use grid layout in the header frame
        header_frame.grid_columnconfigure(0, weight=1)  # left
        header_frame.grid_columnconfigure(1, weight=2)  # center title
        header_frame.grid_columnconfigure(2, weight=1)  # right

        # Title Label (centered)
        title_label = tk.Label(
            header_frame,
            text="Welcome to Safora",
            font=("Cambria", 25, "bold"),
            bg="#1f4e7a",
            fg="white"
        )
        title_label.grid(row=0, column=1, pady=10)

        # Home Label (clickable text, right aligned)
        home_label = tk.Label(
            header_frame,
            text="Home",
            font=("Mulish", 12, "bold"),
            fg="#ffffff",
            bg="#1f4e7a",
            cursor="hand2"
        )
        home_label.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Bind click event
        home_label.bind("<Button-1>", lambda e: self.show_home_screen())

        # Main layout
        main_frame = tk.Frame(self, bg="#d9e6fc")
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main_frame, width=300, bg="#3a699c")
        sidebar.pack(side="left", fill="y")

        # Content placeholder (right side)
        self.content = tk.Frame(main_frame, bg="#d9e6fc")
        self.content.pack(side="right", fill="both", expand=True)

        # Treeview Menu
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        font=("mulish", 11, 'bold'),
                        foreground="#d7dfed",
                        rowheight=30,
                        fieldbackground="#d9e6fc",
                        background="#3a699c")
        style.map('Treeview', background=[('selected', '#1e3d58')])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("Treeview.Heading", font=('Calibri', 14, 'bold'))

        # Replace +/- with arrow symbols (▶ ▼)
        style.configure("Custom.Treeview", indent=10)
        style.layout("Custom.Treeview.Item", [
            ("Treeitem.padding", {
                "children": [("Treeitem.indicator", {}),
                             ("Treeitem.image", {}),
                             ("Treeitem.text", {})],
                "sticky": "nswe"
            })
        ])

        tree = ttk.Treeview(sidebar, show="tree", style="Treeview")
        tree.pack(padx=10, pady=20, fill="y", expand=True)


        customer_id = tree.insert("", "end", text="Customer Master")
        tree.insert(customer_id, "end", text="Create Customer")
        tree.insert(customer_id, "end", text="Delete Customer")
        tree.insert(customer_id, "end", text="Update Customer")
        tree.insert(customer_id, "end", text="View Customer")

        state_id = tree.insert("", "end", text="State Master")
        tree.insert(state_id, "end", text="Create State")
        tree.insert(state_id, "end", text="Delete State")
        tree.insert(state_id, "end", text="View State")


        plan_id = tree.insert("", "end", text="Plan Master")
        tree.insert(plan_id, "end", text="Create Plan")
        tree.insert(plan_id, "end", text="Delete Plan")
        tree.insert(plan_id, "end", text="Update Plan")
        tree.insert(plan_id, "end", text="View Plan")
        
        cp_id = tree.insert("", "end", text="Channel Partner Master")
        tree.insert(cp_id, "end", text="Create Partner")
        tree.insert(cp_id, "end", text="Delete Partner")
        tree.insert(cp_id, "end", text="Update Partner")
        tree.insert(cp_id, "end", text="View Partner")
        
        Branch_id = tree.insert("", "end", text="Branch Master")
        tree.insert(Branch_id, "end", text="Create Branch")
        tree.insert(Branch_id, "end", text="Delete Branch")
        tree.insert(Branch_id, "end", text="Update Branch")
        tree.insert(Branch_id, "end", text="View Branch")


        # employee_id = tree.insert("", "end", text="Employee Master")
        # tree.insert(employee_id, "end", text="Create Employee")
        # tree.insert(employee_id, "end", text="Delete Employee")

        # proposal_id = tree.insert("", "end", text="Proposal")
        # tree.insert(proposal_id, "end", text="Create Proposal")
        
        # dashboard_id = tree.insert("", "end", text="Dashboard")
        
        report_id = tree.insert("", "end", text="Reports")
        tree.insert(report_id, "end", text="Export Report")

        tree.bind("<<TreeviewSelect>>", self.menu_selected)

        # Exit Button
        exit_btn = tk.Button(sidebar, text="Exit", font=("Mulish", 11, 'bold'),
                             bg="#3a699c", fg="white", width=20,
                             command=self.quit)
        exit_btn.pack(pady=10)

        self.tree = tree

    def menu_selected(self, event):
        selected = self.tree.item(self.tree.focus())["text"]
        try:
            if selected == "Create Customer":
                self.load_page_in_content(CustomerApp)
            elif selected == "Delete Customer":
                self.load_page_in_content(DeleteCustomerApp)
            elif selected == "Update Customer":
                self.load_page_in_content(UpdateCustomerApp)
            elif selected == "View Customer":
                self.load_page_in_content(ViewCustomerApp)

            elif selected == "Create Plan":
                self.load_page_in_content(CreatePlanApp)
            elif selected == "Delete Plan":
                self.load_page_in_content(DeletePlanApp)
            elif selected == "Update Plan":
                self.load_page_in_content(UpdatePlanApp)
            elif selected == "View Plan":
                self.load_page_in_content(ViewPlanApp)

            elif selected == "Create Employee":
                self.load_page_in_content(EmployeeApp)
            elif selected == "Delete Employee":
                messagebox.showinfo("Action", "Delete Employee page coming soon!")

            elif selected == "Create Partner":
                self.load_page_in_content(CreatePartnerApp)
            elif selected == "Delete Partner":
                self.load_page_in_content(DeletePartnerApp)
            elif selected == "View Partner":
                self.load_page_in_content(ViewPartnerApp)
            elif selected == "Update Partner":
                self.load_page_in_content(UpdatePartnerApp)    
            
            elif selected == "Create State":
                self.load_page_in_content(CreateStateApp)
            elif selected == "Delete State":
                self.load_page_in_content(DeleteStateApp)
            elif selected == "View State":
                self.load_page_in_content(ViewStateApp)
                
            elif selected == "Create Branch":
                self.load_page_in_content(CreateBranchApp)
            elif selected == "Delete Branch":
                self.load_page_in_content(CreateBranchApp)
            elif selected == "View Branch":
                self.load_page_in_content(CreateBranchApp)

            elif selected == "Create Proposal":
                self.load_page_in_content(ProposalApp)

            elif selected == "Dashboard":
                self.load_page_in_content(DashboardApp)
                
            elif selected == "Export Report":
                self.load_page_in_content(ReportApp)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def load_page_in_content(self, PageClass):
        # Clear existing content
        for widget in self.content.winfo_children():
            widget.destroy()

        # Load new page/frame
        page = PageClass(self.content)
        page.pack(fill="both", expand=True)

    def show_home_screen(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        welcome_label = tk.Label(
            self.content,
            text="Welcome to Safora Life Insurance System",
            font=("Cambria", 22, "bold"),
            bg="#d9e6fc",
            fg="#1f4e7a",
            pady=50
        )
        welcome_label.pack(expand=True)


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()