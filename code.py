import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import pandas as pd
import plotly.express as px
import os
import kaleido

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        self.data = pd.DataFrame(columns=["Date", "Category", "Amount"])
        self.current_category = ""
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        
        self.date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        date_label = tk.Label(self.left_frame, text="Date", bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold"))
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = tk.Entry(self.left_frame, textvariable=self.date_var, font=("Arial", 12))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        category_label = tk.Label(self.left_frame, text="Category", bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold"))
        category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_entry = tk.Entry(self.left_frame, textvariable=self.category_var, font=("Arial", 12))
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        amount_label = tk.Label(self.left_frame, text="Amount", bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold"))
        amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = tk.Entry(self.left_frame, textvariable=self.amount_var, font=("Arial", 12))
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

     
        self.add_button = tk.Button(self.left_frame, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.add_button.grid(row=3, column=1, padx=5, pady=5)

        self.edit_button = tk.Button(self.left_frame, text="Edit Expense", command=self.edit_expense, bg="#2196F3", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.edit_button.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.left_frame, text="Delete Expense", command=self.delete_expense, bg="#F44336", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.delete_button.grid(row=5, column=1, padx=5, pady=5)

        self.summary_button = tk.Button(self.left_frame, text="Summary", command=self.summary, bg="#9C27B0", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.summary_button.grid(row=6, column=1, padx=5, pady=5)

        self.category_button = tk.Button(self.left_frame, text="Manage Categories", command=self.manage_categories, bg="#FFC107", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.category_button.grid(row=7, column=1, padx=5, pady=5)

        self.chart_button = tk.Button(self.left_frame, text="View Charts", command=self.view_charts, bg="#009688", fg="#FFFFFF", font=("Arial", 12, "bold"), relief="raised")
        self.chart_button.grid(row=8, column=1, padx=5, pady=5)

        self.table_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.table_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.create_table()

        self.pie_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.pie_frame.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Map>", self.on_window_mapped)

    def create_table(self):
        self.table = ttk.Treeview(self.table_frame, columns=("Date", "Category", "Amount"), show="headings")
        self.table.heading("Date", text="Date")
        self.table.heading("Category", text="Category")
        self.table.heading("Amount", text="Amount")
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scroll_y.set)

        for row in self.data.itertuples(index=False):
            self.table.insert("", "end", values=row)

    def on_window_mapped(self, event):
        if self.root.winfo_width() >= 1000:
            self.update_pie_chart()
            self.pie_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.pie_frame.pack_forget()

    def update_pie_chart(self):
        daily_data = self.data
        daily_pie = px.pie(daily_data, values="Amount", names="Category", title="Daily Expense Spending")
        daily_pie.update_layout(width=400, height=400)
        daily_pie.update_traces(textposition="inside", textinfo="percent+label")

        self.pie_canvas = tk.Canvas(self.pie_frame, bg="#f0f0f0")
        self.pie_canvas.pack(fill=tk.BOTH, expand=True)

        daily_pie.write_image("pie_chart.png")
        pie_image = tk.PhotoImage(file="pie_chart.png")
        self.pie_canvas.create_image(0, 0, anchor=tk.NW, image=pie_image)
        self.pie_canvas.image = pie_image

    def add_expense(self):
        self._add_or_edit_expense(True)

    def edit_expense(self):
        self._add_or_edit_expense(False)

    def _add_or_edit_expense(self, is_adding):
        date = self.date_var.get()
        category = self.category_var.get()
        amount = self.amount_var.get()

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount input. Please enter a valid number.")
            return

        if not date or not category or amount <= 0:
            messagebox.showerror("Error", "Invalid input")
            return

        if is_adding:
            self.data = self.data.append({"Date": date, "Category": category, "Amount": amount}, ignore_index=True)
        else:
            index = self.data.index[(self.data["Date"] == date) & (self.data["Category"] == category)]
            if len(index) == 0:
                messagebox.showerror("Error", "Expense not found")
                return

            self.data.loc[index, "Amount"] = amount

        self.clear_entries()

    def delete_expense(self):
        date = self.date_var.get()
        category = self.category_var.get()

        index = self.data.index[(self.data["Date"] == date) & (self.data["Category"] == category)]
        if len(index) == 0:
            messagebox.showerror("Error", "Expense not found")
            return

        self.data.drop(index, inplace=True)
        self.clear_entries()

    def summary(self):
        summary = self.data.groupby(["Category"]).sum()
        summary["Amount"] = summary["Amount"].round(2)
        messagebox.showinfo("Summary", summary.to_string())

    def manage_categories(self):
        categories = self.data["Category"].unique().tolist()
        categories_string = ", ".join(categories)
        messagebox.showinfo("Manage Categories", categories_string)

    def view_charts(self):
        if len(self.data) == 0:
            messagebox.showerror("Error", "No data available to create charts")
            return

        today = datetime.date.today()
        week = today - datetime.timedelta(days=today.weekday())
        month = today.replace(day=1)
        year = today.replace(month=1, day=1)

        daily_data = self.data[(self.data["Date"] == today.strftime("%Y-%m-%d"))]
        weekly_data = self.data[(self.data["Date"] >= week.strftime("%Y-%m-%d")) & (self.data["Date"] <= today.strftime("%Y-%m-%d"))]
        monthly_data = self.data[(self.data["Date"] >= month.strftime("%Y-%m-%d"))]
        yearly_data = self.data[(self.data["Date"] >= year.strftime("%Y-%m-%d"))]

        px.line(daily_data, x="Date", y="Amount", color="Category", title="Daily Expenses").show()
        px.line(weekly_data, x="Date", y="Amount", color="Category", title="Weekly Expenses").show()
        px.line(monthly_data, x="Date", y="Amount", color="Category", title="Monthly Expenses").show()
        px.line(yearly_data, x="Date", y="Amount", color="Category", title="Yearly Expenses").show()

        self.clear_entries()

    def clear_entries(self):
        self.date_var.set("")
        self.category_var.set("")
        self.amount_var.set("")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1000x600")
        self.configure(bg="#f0f0f0")

    def run_headlessly(self):
        while True:
            self.update_idletasks()
            self.update()

if __name__ == "__main__":
    app = Application()
    app.run_headlessly()
