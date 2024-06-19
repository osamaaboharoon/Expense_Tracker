import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Fetching currency rates from the API
        self.currency_rates = self.get_currency_rates()

        # Creating the UI elements
        self.create_widgets()

    def get_currency_rates(self):
        """
        Get currency exchange rates from an external API.
        Returns:
            dict: A dictionary with currency codes as keys and exchange rates as values.
        """
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"]

    def create_widgets(self):
        """
        Create and place the widgets (labels, entry fields, buttons, and treeview) in the GUI.
        """
        # Amount label and entry
        ttk.Label(self.root, text="Amount").grid(row=0, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        # Currency label and combobox
        ttk.Label(self.root, text="Currency").grid(row=1, column=0, padx=10, pady=5)
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self.root, textvariable=self.currency_var)
        self.currency_combo['values'] = list(self.currency_rates.keys())
        self.currency_combo.grid(row=1, column=1, padx=10, pady=5)

        # Category label and combobox
        ttk.Label(self.root, text="Category").grid(row=2, column=0, padx=10, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_combo['values'] = ["life expenses", "electricity", "gas", "rental", "grocery", "savings", "education", "charity"]
        self.category_combo.grid(row=2, column=1, padx=10, pady=5)

        # Payment Method label and combobox
        ttk.Label(self.root, text="Payment Method").grid(row=3, column=0, padx=10, pady=5)
        self.payment_var = tk.StringVar()
        self.payment_combo = ttk.Combobox(self.root, textvariable=self.payment_var)
        self.payment_combo['values'] = ["Cash", "Credit Card", "Paypal"]
        self.payment_combo.grid(row=3, column=1, padx=10, pady=5)

        # Date label and entry
        ttk.Label(self.root, text="Date").grid(row=4, column=0, padx=10, pady=5)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Add Expense button
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, column=1, padx=10, pady=5)

        # Treeview to display expenses
        self.tree = ttk.Treeview(self.root, columns=("amount", "currency", "category", "payment"), show="headings")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("currency", text="Currency")
        self.tree.heading("category", text="Category")
        self.tree.heading("payment", text="Payment Method")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Configure the total row with a yellow background
        self.tree.tag_configure("total", background="yellow")

    def add_expense(self):
        """
        Add a new expense to the treeview and update the total expenses.
        """
        amount = float(self.amount_entry.get())
        currency = self.currency_var.get()
        category = self.category_var.get()
        payment = self.payment_var.get()
        date = self.date_entry.get()

        usd_amount = amount * self.currency_rates.get(currency, 1)

        # Insert new expense into the treeview
        self.tree.insert("", "end", values=(amount, currency, category, payment))

        # Update total expenses in USD
        self.update_total_expenses()

        # Clear entry fields after adding expense
        self.clear_entries()

    def update_total_expenses(self):
        """
        Calculate and display the total expenses in USD.
        """
        total = 0
        for child in self.tree.get_children():
            amount, currency = self.tree.item(child)["values"][:2]
            usd_amount = float(amount) * self.currency_rates.get(currency, 1)
            total += usd_amount

        # Remove existing total row if it exists
        for item in self.tree.get_children():
            if self.tree.item(item)["tags"] == ("total",):
                self.tree.delete(item)

        # Insert new total row
        self.tree.insert("", "end", values=(round(total, 2), "USD", "", ""), tags=("total",))

    def clear_entries(self):
        """
        Clear the input fields for the next entry.
        """
        self.amount_entry.delete(0, tk.END)
        self.currency_var.set('')
        self.category_var.set('')
        self.payment_var.set('')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
