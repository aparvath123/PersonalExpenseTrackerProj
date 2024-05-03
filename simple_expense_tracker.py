import tkinter as tk
from tkinter import ttk, messagebox
import csv
from os import path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from collections import defaultdict

# Define functions
def add_transaction():
    description = description_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()
    if description and amount and date:
        try:
            amount_float = float(amount)
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
            transaction = f"{date}, {description}, ${amount_float:.2f}"
            transactions_list.insert(tk.END, transaction)
            description_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            save_transaction(date, description, amount_float)
            update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount or date (YYYY-MM-DD)")

def save_transaction(date, description, amount):
    with open("transactions.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])

def load_transactions():
    transactions_list.delete(0, tk.END)
    if path.exists("transactions.csv"):
        with open("transactions.csv", newline='') as file:
            reader = csv.reader(file)
            for date, description, amount in reader:
                transaction = f"{date}, {description}, ${float(amount):.2f}"
                transactions_list.insert(tk.END, transaction)

def show_frame(frame):
    frame.tkraise()

def update_dashboard():
    try:
        current_budget = float(budget_entry.get())
    except ValueError:
        current_budget = 0  # Default to 0 if the input is invalid
    total_expense = 0
    if path.exists("transactions.csv"):
        with open("transactions.csv", newline='') as file:
            reader = csv.reader(file)
            for date, description, amount in reader:
                total_expense += float(amount)
    total_expenses_var.set(f"Total Expenses: ${total_expense:.2f}")
    net_budget_var.set(f"Remaining Budget: ${current_budget - total_expense:.2f}")


def plot_graph():
    expenses_by_description = defaultdict(float)

    # Load transactions and aggregate by description
    if path.exists("transactions.csv"):
        with open("transactions.csv", newline='') as file:
            reader = csv.reader(file)
            for date_str, description, amount in reader:
                expenses_by_description[description] += float(amount)

    
    # Ensure we have data to plot
    if not expenses_by_description:
        messagebox.showinfo("No Data", "There are no expense data to display.")
        return
    
    # Data for pie chart (descriptions and amounts)
    labels = list(expenses_by_description.keys())
    sizes = list(expenses_by_description.values())

    # Plotting
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    
    # Make the labels best fit
    plt.setp(texts, size='small')
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

    # Embedding the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)





# Initial setup
root = tk.Tk()
root.title("Simple Expense Tracker")
root.geometry("650x520")

# Variables
total_expenses_var = tk.StringVar()
net_budget_var = tk.StringVar()

# Frames
main_menu_frame = tk.Frame(root)
add_transaction_frame = tk.Frame(root)
dashboard_frame = tk.Frame(root)
graph_frame = tk.Frame(root)

for frame in (main_menu_frame, add_transaction_frame, dashboard_frame, graph_frame):
    frame.grid(row=0, column=0, sticky='nsew')


# Main menu frame setup
main_menu_frame = tk.Frame(root)
main_menu_frame.grid(row=0, column=0, sticky='nsew')

# Personal Expense Tracker title
personal_title_label = tk.Label(main_menu_frame, text="Personal Expense Tracker", font=('Arial', 24))
personal_title_label.pack(pady=(10, 20))  # Adjust padding as needed




# Main menu
title_label = tk.Label(main_menu_frame, text="Main Menu", font=('Arial', 24))
title_label.pack(pady=20)

budget_label = tk.Label(main_menu_frame, text="Set Your Budget:")
budget_label.pack()
budget_entry = ttk.Entry(main_menu_frame)
budget_entry.pack()

add_transaction_button = ttk.Button(main_menu_frame, text="Add Transaction", command=lambda: show_frame(add_transaction_frame))
add_transaction_button.pack()
dashboard_button = ttk.Button(main_menu_frame, text="View Dashboard", command=lambda: [show_frame(dashboard_frame), update_dashboard()])
dashboard_button.pack()
graph_button = ttk.Button(main_menu_frame, text="View Graph", command=lambda: [show_frame(graph_frame), plot_graph()])
graph_button.pack()

# Add transaction
description_label = ttk.Label(add_transaction_frame, text="Description:")
description_label.pack()
description_entry = ttk.Entry(add_transaction_frame)
description_entry.pack()

amount_label = ttk.Label(add_transaction_frame, text="Amount:")
amount_label.pack()
amount_entry = ttk.Entry(add_transaction_frame)
amount_entry.pack()

date_label = ttk.Label(add_transaction_frame, text="Date (YYYY-MM-DD):")
date_label.pack()
date_entry = ttk.Entry(add_transaction_frame)
date_entry.pack()

add_button = ttk.Button(add_transaction_frame, text="Add Transaction", command=add_transaction)
add_button.pack()

transactions_list = tk.Listbox(add_transaction_frame)
transactions_list.pack()

back_button = ttk.Button(add_transaction_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame))
back_button.pack(pady=10)

# Dashboard
expenses_label = ttk.Label(dashboard_frame, textvariable=total_expenses_var)
expenses_label.pack()

budget_label = ttk.Label(dashboard_frame, textvariable=net_budget_var)
budget_label.pack()

back_dashboard_button = ttk.Button(dashboard_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame))
back_dashboard_button.pack()

# Graph
back_graph_button = ttk.Button(graph_frame, text="Back to Main Menu", command=lambda: show_frame(main_menu_frame))
back_graph_button.pack()

# Start
load_transactions()
show_frame(main_menu_frame)

root.mainloop()

