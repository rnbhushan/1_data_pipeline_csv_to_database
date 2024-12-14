import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

class UserAccessManager:
    def __init__(self, historical_data_path):
        """
        Initialize User Access Manager
        
        Args:
            historical_data_path (str): Path to historical access data CSV
        """
        self.historical_data = pd.read_csv(historical_data_path)
        
    def check_website_access(self, website):
        """
        Check website access and return user details
        
        Args:
            website (str): Website to check access for
        
        Returns:
            tuple: (approval_status, user_details_dataframe)
        """
        # Filter data for the specific website
        website_data = self.historical_data[
            self.historical_data['Website'].str.contains(website, case=False)
        ]
        
        # Check if website has any access records
        if website_data.empty:
            return "Cannot approve: No access records found", pd.DataFrame()
        
        # Check approved status
        approved_data = website_data[website_data['RequestStatus'] == 'Approved']
        
        if approved_data.empty:
            return "Cannot approve: No approved access found", website_data
        
        # Prepare approval status
        approval_status = f"We can approve: {len(approved_data)} user(s) have access to {website}"
        
        return approval_status, approved_data
    
    def create_gui(self):
        """Create Tkinter GUI for access request"""
        root = tk.Tk()
        root.title("Detailed Website Access Checker")
        root.geometry("800x600")
        
        # Style
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        
        # Website Input Frame
        input_frame = ttk.Frame(root)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        # Website Input
        ttk.Label(input_frame, text="Enter Website:").pack(side=tk.LEFT, padx=5)
        website_entry = ttk.Entry(input_frame, width=40)
        website_entry.pack(side=tk.LEFT, padx=5)
        
        # Approval Status Label
        approval_status_label = ttk.Label(root, text="", font=("Arial", 12, "bold"))
        approval_status_label.pack(pady=10)
        
        # Results Frame
        results_frame = ttk.LabelFrame(root, text="User Access Details")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Columns to display
        columns = (
            'UserID', 'Name', 'Email', 'Department', 
            'ReportingManager', 'RequestStatus'
        )
        
        # Treeview to display results
        results_tree = ttk.Treeview(results_frame, columns=columns, show='headings')
        
        # Configure column headings
        column_names = {
            'UserID': 'User ID',
            'Name': 'Name',
            'Email': 'Email',
            'Department': 'Department',
            'ReportingManager': 'Reporting Manager',
            'RequestStatus': 'Request Status'
        }
        
        for col in columns:
            results_tree.heading(col, text=column_names[col])
            results_tree.column(col, width=100)
        
        results_tree.pack(fill='both', expand=True)
        
        # Scrollbar for results
        scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=results_tree.xview)
        results_tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        def submit_request():
            """Handle access request submission"""
            # Clear previous results
            approval_status_label.config(text="")
            for i in results_tree.get_children():
                results_tree.delete(i)
            
            # Get input website
            input_website = website_entry.get().strip()
            
            if not input_website:
                messagebox.showwarning("Input Error", "Please enter a website")
                return
            
            # Check website access
            approval_status, user_data = self.check_website_access(input_website)
            
            # Update approval status
            approval_status_label.config(text=approval_status)
            
            # Populate results
            if not user_data.empty:
                for _, row in user_data.iterrows():
                    results_tree.insert('', 'end', values=(
                        row['UserID'], row['Name'], row['Email'], 
                        row['Department'], row['ReportingManager'], 
                        row['RequestStatus']
                    ))
        
        def clear_fields():
            """Clear input and results"""
            website_entry.delete(0, tk.END)
            approval_status_label.config(text="")
            for i in results_tree.get_children():
                results_tree.delete(i)
        
        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(padx=10, pady=10)
        
        # Submit Button
        submit_btn = ttk.Button(button_frame, text="Submit", command=submit_request)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = ttk.Button(button_frame, text="Clear", command=clear_fields)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        root.mainloop()

# Usage example
if __name__ == "__main__":
    access_manager = UserAccessManager('user_access_historical_data.csv')
    access_manager.create_gui()