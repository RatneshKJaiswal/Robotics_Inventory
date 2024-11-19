import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import hashlib

# Dark Theme Styling
BG_COLOR = "#1f1f1f"
FG_COLOR = "#eaeaea"
ENTRY_BG = "#333333"
BTN_BG = "#3c3c3c"
BTN_FG = "#ffffff"
HEADER_FONT = ("Poppins", 15, "bold")
LABEL_FONT = ("Poppins", 11)
BUTTON_FONT = ("Poppins", 12, "bold")


# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ratx100",
        database="robotics_inventory"
    )


# Log Transaction
def log_transaction(product_id, quantity, transaction_type, person_name, roll_number):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO transactions (product_id, quantity, transaction_type, person_name, roll_number)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, quantity, transaction_type, person_name, roll_number))
    db.commit()
    db.close()


# Home Page
# Home Page
def show_home():
    home = tk.Tk()
    home.title("Robotics Inventory - Home")
    home.geometry("400x400")
    home.configure(bg=BG_COLOR)

    tk.Label(home, text="Robotics Inventory System", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    tk.Button(home, text="Add/Return Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=show_add_return).pack(pady=10)
    tk.Button(home, text="Delete Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=show_delete).pack(pady=10)
    tk.Button(home, text="Issue Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=show_issue).pack(pady=10)
    tk.Button(home, text="View Inventory", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=show_view_inventory).pack(pady=10)
    tk.Button(home, text="View Transactions", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=show_view_transactions).pack(pady=10)

    home.mainloop()

# View Inventory Page
def show_view_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("600x400")
    inventory_window.configure(bg=BG_COLOR)

    tk.Label(inventory_window, text="Inventory", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    # Table for displaying inventory
    tree = ttk.Treeview(inventory_window, columns=("Product ID", "Product Name", "Quantity"), show="headings")
    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Quantity", text="Quantity")
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch data from inventory
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT product_id, product_name, quantity FROM inventory")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    db.close()

# View Transactions Page
# View Transactions Page
def show_view_transactions():
    transactions_window = tk.Toplevel()
    transactions_window.title("Transactions")
    transactions_window.geometry("1400x500")
    transactions_window.configure(bg=BG_COLOR)

    tk.Label(transactions_window, text="Transactions", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    # Table for displaying transactions
    tree = ttk.Treeview(transactions_window, columns=("Transaction ID", "Product ID", "Product Name", "Quantity", "Type", "Person", "Roll Number"), show="headings")
    tree.heading("Transaction ID", text="Transaction ID")
    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Type", text="Transaction Type")
    tree.heading("Person", text="Person Name")
    tree.heading("Roll Number", text="Roll Number")
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch data from transactions with product names
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.transaction_id, t.product_id, i.product_name, t.quantity, t.transaction_type, t.person_name, t.roll_number
        FROM transactions t
        JOIN inventory i ON t.product_id = i.product_id
        ORDER BY t.transaction_id DESC
    """)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    db.close()


# Add/Return Product Page
def show_add_return():
    def add_product():
        product_name = product_name_entry.get()
        quantity = int(quantity_entry.get())
        person_name = person_name_entry.get()
        roll_number = roll_number_entry.get()

        db = connect_db()
        cursor = db.cursor()

        # Check if product exists, then add or update
        cursor.execute("SELECT product_id, quantity FROM inventory WHERE product_name = %s", (product_name,))
        result = cursor.fetchone()
        if result:
            product_id, current_quantity = result
            new_quantity = current_quantity + quantity
            cursor.execute("UPDATE inventory SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        else:
            cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)", (product_name, quantity))
            product_id = cursor.lastrowid

        db.commit()
        log_transaction(product_id, quantity, 'add', person_name, roll_number)
        db.close()
        messagebox.showinfo("Success", "Product added successfully.")

    add_window = tk.Toplevel()
    add_window.title("Add/Return Product")
    add_window.geometry("500x500")
    add_window.configure(bg=BG_COLOR)

    tk.Label(add_window, text="Add/Return Product", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    tk.Label(add_window, text="Product Name", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    product_name_entry = tk.Entry(add_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    product_name_entry.pack(pady=5)

    tk.Label(add_window, text="Quantity", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    quantity_entry = tk.Entry(add_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    quantity_entry.pack(pady=5)

    tk.Label(add_window, text="Person Name", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    person_name_entry = tk.Entry(add_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    person_name_entry.pack(pady=5)

    tk.Label(add_window, text="Roll Number", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    roll_number_entry = tk.Entry(add_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    roll_number_entry.pack(pady=5)

    tk.Button(add_window, text="Add Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=add_product).pack(pady=10)


# Delete Product Page
def show_delete():
    def delete_product():
        product_id = int(product_id_entry.get())
        person_name = person_name_entry.get()
        roll_number = roll_number_entry.get()

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT product_name, quantity FROM inventory WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        if result:
            product_name, quantity = result
            cursor.execute("DELETE FROM inventory WHERE product_id = %s", (product_id,))
            db.commit()
            log_transaction(product_id, quantity, 'delete', person_name, roll_number)
            messagebox.showinfo("Success", "Product deleted successfully.")
        else:
            messagebox.showwarning("Warning", "Product not found.")

        db.close()

    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("400x400")
    delete_window.configure(bg=BG_COLOR)

    tk.Label(delete_window, text="Delete Product", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    tk.Label(delete_window, text="Product ID", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    product_id_entry = tk.Entry(delete_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    product_id_entry.pack(pady=5)

    tk.Label(delete_window, text="Person Name", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    person_name_entry = tk.Entry(delete_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    person_name_entry.pack(pady=5)

    tk.Label(delete_window, text="Roll Number", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    roll_number_entry = tk.Entry(delete_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    roll_number_entry.pack(pady=5)

    tk.Button(delete_window, text="Delete Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG,
              command=delete_product).pack(pady=10)


# Issue Product Page
def show_issue():
    def issue_product():
        product_id = int(product_id_entry.get())
        quantity = int(quantity_entry.get())
        person_name = person_name_entry.get()
        roll_number = roll_number_entry.get()

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT product_name, quantity FROM inventory WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        if result:
            product_name, current_quantity = result
            if current_quantity >= quantity:
                new_quantity = current_quantity - quantity
                cursor.execute("UPDATE inventory SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
                db.commit()
                log_transaction(product_id, quantity, 'issue', person_name, roll_number)
                messagebox.showinfo("Success", "Product issued successfully.")
            else:
                messagebox.showwarning("Warning", "Insufficient stock available.")
        else:
            messagebox.showwarning("Warning", "Product not found.")

        db.close()

    issue_window = tk.Toplevel()
    issue_window.title("Issue Product")
    issue_window.geometry("500x500")
    issue_window.configure(bg=BG_COLOR)

    tk.Label(issue_window, text="Issue Product", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

    tk.Label(issue_window, text="Product ID", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    product_id_entry = tk.Entry(issue_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    product_id_entry.pack(pady=5)

    tk.Label(issue_window, text="Quantity", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    quantity_entry = tk.Entry(issue_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    quantity_entry.pack(pady=5)

    tk.Label(issue_window, text="Person Name", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    person_name_entry = tk.Entry(issue_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    person_name_entry.pack(pady=5)

    tk.Label(issue_window, text="Roll Number", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
    roll_number_entry = tk.Entry(issue_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
    roll_number_entry.pack(pady=5)

    tk.Button(issue_window, text="Issue Product", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=issue_product).pack(
        pady=10)


# Main Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()
    password_hash = password

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = %s AND password_hash = %s", (username, password_hash))
    result = cursor.fetchone()
    db.close()

    if result:
        login_window.destroy()
        show_home()
    else:
        messagebox.showerror("Error", "Invalid username or password.")


# Login Window
login_window = tk.Tk()
login_window.title("Robotics Inventory Login")
login_window.geometry("400x300")
login_window.configure(bg=BG_COLOR)

tk.Label(login_window, text="Login", font=HEADER_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
tk.Label(login_window, text="Username", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
username_entry = tk.Entry(login_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
password_entry = tk.Entry(login_window, font=LABEL_FONT, bg=ENTRY_BG, fg=FG_COLOR, show="*")
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", font=BUTTON_FONT, bg=BTN_BG, fg=BTN_FG, command=login).pack(pady=20)


login_window.mainloop()