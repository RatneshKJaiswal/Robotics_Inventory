import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import hashlib
from datetime import datetime
from tkinter import *

root = Tk()
product_id_entry = Entry(root)
quantity_entry = Entry(root)
person_name_entry = Entry(root)
roll_number_entry = Entry(root)


# Enhanced Modern Theme
class Theme:
    # Main colors
    PRIMARY = "#2c3e50"  # Dark blue-grey
    SECONDARY = "#34495e"  # Lighter blue-grey
    ACCENT = "#3498db"  # Bright blue
    SUCCESS = "#2ecc71"  # Green
    WARNING = "#e74c3c"  # Red

    # Background colors
    BG_DARK = "#1a1a1a"
    BG_LIGHT = "#2d2d2d"

    # Text colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#ecf0f1"
    TEXT_MUTED = "#bdc3c7"

    # Fonts
    FONT_FAMILY = "Helvetica"
    HEADER_FONT = (FONT_FAMILY, 20, "bold")
    SUBHEADER_FONT = (FONT_FAMILY, 16, "bold")
    BODY_FONT = (FONT_FAMILY, 12)
    BUTTON_FONT = (FONT_FAMILY, 12, "bold")


# Custom Styles
def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')

    # Configure Treeview
    style.configure("Treeview",
                    background=Theme.BG_LIGHT,
                    foreground=Theme.TEXT_PRIMARY,
                    fieldbackground=Theme.BG_LIGHT,
                    font=Theme.BODY_FONT)

    style.configure("Treeview.Heading",
                    background=Theme.SECONDARY,
                    foreground=Theme.TEXT_PRIMARY,
                    font=Theme.BUTTON_FONT)

    # Configure buttons
    style.configure("Accent.TButton",
                    background=Theme.ACCENT,
                    foreground=Theme.TEXT_PRIMARY,
                    font=Theme.BUTTON_FONT,
                    padding=10)


# Custom Button Class
class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.update({
            'bg': Theme.ACCENT,
            'fg': Theme.TEXT_PRIMARY,
            'font': Theme.BUTTON_FONT,
            'borderwidth': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'
        })
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.config(bg=Theme.SECONDARY)

    def on_leave(self, event):
        self.config(bg=Theme.ACCENT)


# Custom Entry Class
class ModernEntry(tk.Entry):
    def __init__(self, master, **kwargs):
        kwargs.update({
            'bg': Theme.BG_LIGHT,
            'fg': Theme.TEXT_PRIMARY,
            'font': Theme.BODY_FONT,
            'insertbackground': Theme.TEXT_PRIMARY,
            'borderwidth': 0,
            'highlightthickness': 1,
            'highlightcolor': Theme.ACCENT,
            'highlightbackground': Theme.SECONDARY
        })
        super().__init__(master, **kwargs)


# Database Connection (unchanged)
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ratx100",
        database="robotics_inventory"
    )


# Enhanced Home Page
def show_home():
    home = tk.Tk()
    home.title("Robotics Inventory System")
    home.geometry("800x600")
    home.configure(bg=Theme.BG_DARK)

    # Create main container
    main_frame = tk.Frame(home, bg=Theme.BG_DARK)
    main_frame.pack(expand=True, fill='both', padx=40, pady=40)

    # Header
    header_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
    header_frame.pack(fill='x', pady=(0, 30))

    tk.Label(header_frame,
             text="Robotics Inventory System",
             font=Theme.HEADER_FONT,
             fg=Theme.TEXT_PRIMARY,
             bg=Theme.BG_DARK).pack()

    tk.Label(header_frame,
             text="Manage your inventory efficiently",
             font=Theme.BODY_FONT,
             fg=Theme.TEXT_MUTED,
             bg=Theme.BG_DARK).pack(pady=(5, 0))

    # Buttons Container
    button_frame = tk.Frame(main_frame, bg=Theme.BG_DARK)
    button_frame.pack(expand=True)

    # Grid of buttons
    buttons = [
        ("Add/Return Product", show_add_return),
        ("Issue Product", show_issue),
        ("Delete Product", show_delete),
        ("View Inventory", show_view_inventory),
        ("View Transactions", show_view_transactions)
    ]

    for idx, (text, command) in enumerate(buttons):
        row = idx // 2
        col = idx % 2
        btn = ModernButton(button_frame, text=text, command=command)
        btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

    # Configure grid
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    # Status bar
    status_frame = tk.Frame(main_frame, bg=Theme.BG_LIGHT)
    status_frame.pack(fill='x', side='bottom', pady=(20, 0))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tk.Label(status_frame,
             text=f"Last updated: {current_time}",
             font=Theme.BODY_FONT,
             fg=Theme.TEXT_MUTED,
             bg=Theme.BG_LIGHT).pack(pady=10)

    home.mainloop()

def log_transaction(product_id, quantity, transaction_type, person_name, roll_number):
    """
    Logs a transaction in the database.
    Parameters:
    - product_id (int): The ID of the product.
    - quantity (int): The quantity of the transaction.
    - transaction_type (str): Type of transaction ('add', 'issue', 'delete', etc.).
    - person_name (str): Name of the person involved in the transaction.
    - roll_number (str): Roll number of the person.

    """
    try:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # Insert transaction into the database
        cursor.execute("""
            INSERT INTO transactions (product_id, quantity, transaction_type, person_name, roll_number, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, quantity, transaction_type, person_name, roll_number, timestamp))

        # Commit the transaction
        db.commit()
        db.close()
    except Exception as e:
        # Display an error message for logging failure
        messagebox.showerror("Error", f"Failed to log transaction: {e}")

# Enhanced View Inventory Page
def show_view_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("1000x600")
    inventory_window.configure(bg=Theme.BG_DARK)

    # Header
    tk.Label(inventory_window,
             text="Current Inventory",
             font=Theme.HEADER_FONT,
             fg=Theme.TEXT_PRIMARY,
             bg=Theme.BG_DARK).pack(pady=20)

    # Search frame
    search_frame = tk.Frame(inventory_window, bg=Theme.BG_DARK)
    search_frame.pack(fill='x', padx=20, pady=10)

    tk.Label(search_frame,
             text="Search:",
             font=Theme.BODY_FONT,
             fg=Theme.TEXT_PRIMARY,
             bg=Theme.BG_DARK).pack(side='left', padx=(0, 10))

    search_entry = ModernEntry(search_frame)
    search_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))

    # Table frame
    table_frame = tk.Frame(inventory_window, bg=Theme.BG_DARK)
    table_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side='right', fill='y')

    # Enhanced Treeview
    columns = ("Product ID", "Product Name", "Quantity", "Status")
    tree = ttk.Treeview(table_frame,
                        columns=columns,
                        show="headings",
                        yscrollcommand=scrollbar.set)

    # Configure columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    tree.pack(fill='both', expand=True)
    scrollbar.config(command=tree.yview)

    # Fetch and display data
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT product_id, product_name, quantity FROM inventory")

    for row in cursor.fetchall():
        product_id, name, quantity = row
        status = "Low Stock" if quantity < 5 else "Available"
        tree.insert("", "end", values=(*row, status))

    db.close()

    # Add refresh button
    # refresh_btn = ModernButton(inventory_window,
    #                            text="Refresh",
    #                            command=lambda: refresh_inventory(tree))
    # refresh_btn.pack(pady=20)


# Enhanced Versions of the Functions

def login(username, password, login_window):
    """Login functionality with enhanced UI and error handling."""
    password_hash = password  # Simulate hashing for demonstration purposes

    try:
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
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during login: {e}")


def show_add_return():
    """Add/Return Product functionality with enhanced UI."""
    def add_product():
        product_name = product_name_entry.get()
        quantity = quantity_entry.get()
        person_name = person_name_entry.get()
        roll_number = roll_number_entry.get()

        if not product_name or not quantity.isdigit() or not person_name or not roll_number:
            messagebox.showwarning("Warning", "Please fill in all fields correctly.")
            return

        quantity = int(quantity)
        try:
            db = connect_db()
            cursor = db.cursor()
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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    # UI
    window = tk.Toplevel()
    window.title("Add/Return Product")
    window.geometry("500x400")
    window.configure(bg=Theme.BG_DARK)

    tk.Label(window, text="Add/Return Product", font=Theme.HEADER_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(pady=10)
    fields = [("Product Name", "product_name_entry"), ("Quantity", "quantity_entry"),
              ("Person Name", "person_name_entry"), ("Roll Number", "roll_number_entry")]

    entries = {}
    for label_text, var_name in fields:
        frame = tk.Frame(window, bg=Theme.BG_DARK)
        frame.pack(fill='x', pady=5, padx=20)

        tk.Label(frame, text=label_text, font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w')
        entries[var_name] = ModernEntry(frame)
        entries[var_name].pack(fill='x', pady=5)

    product_name_entry, quantity_entry, person_name_entry, roll_number_entry = (
        entries["product_name_entry"], entries["quantity_entry"], entries["person_name_entry"], entries["roll_number_entry"]
    )
    ModernButton(window, text="Add Product", command=add_product).pack(pady=10)


def show_issue():
    """Issue Product functionality with enhanced UI."""
    def issue_product():
        product_id = product_id_entry.get().strip()
        quantity = quantity_entry.get().strip()
        person_name = person_name_entry.get().strip()
        roll_number = roll_number_entry.get().strip()

        # Validation
        if not product_id.isdigit():
            messagebox.showwarning("Warning", "Product ID must be a valid number.")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showwarning("Warning", "Quantity must be a positive number.")
            return
        if not person_name or not roll_number:
            messagebox.showwarning("Warning", "Person Name and Roll Number cannot be empty.")
            return

        product_id = int(product_id)
        quantity = int(quantity)

        try:
            db = connect_db()
            cursor = db.cursor()

            # Check if product exists and has enough quantity
            cursor.execute("SELECT product_name, quantity FROM inventory WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()

            if result:
                product_name, current_quantity = result
                if current_quantity >= quantity:
                    # Update the product's quantity in inventory
                    new_quantity = current_quantity - quantity
                    cursor.execute("UPDATE inventory SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
                    db.commit()

                    # Log the transaction
                    log_transaction(product_id, quantity, 'issue', person_name, roll_number)
                    messagebox.showinfo("Success", f"Successfully issued {quantity} of '{product_name}'.")
                else:
                    messagebox.showwarning("Warning", f"Insufficient stock. Only {current_quantity} available.")
            else:
                messagebox.showwarning("Warning", "Product not found.")

            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue product: {e}")

    # UI
    issue_window = tk.Toplevel()
    issue_window.title("Issue Product")
    issue_window.geometry("500x500")
    issue_window.configure(bg=Theme.BG_DARK)

    tk.Label(issue_window, text="Issue Product", font=Theme.HEADER_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(pady=10)

    # Product ID Field
    tk.Label(issue_window, text="Product ID", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w', padx=20)
    product_id_entry = ModernEntry(issue_window)
    product_id_entry.pack(fill='x', pady=5, padx=20)

    # Quantity Field
    tk.Label(issue_window, text="Quantity", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w', padx=20)
    quantity_entry = ModernEntry(issue_window)
    quantity_entry.pack(fill='x', pady=5, padx=20)

    # Person Name Field
    tk.Label(issue_window, text="Person Name", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w', padx=20)
    person_name_entry = ModernEntry(issue_window)
    person_name_entry.pack(fill='x', pady=5, padx=20)

    # Roll Number Field
    tk.Label(issue_window, text="Roll Number", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w', padx=20)
    roll_number_entry = ModernEntry(issue_window)
    roll_number_entry.pack(fill='x', pady=5, padx=20)

    # Issue Button
    ModernButton(issue_window, text="Issue Product", command=issue_product).pack(pady=20)



def show_delete():
    """Delete Product functionality with enhanced UI."""
    def delete_product():
        product_id = product_id_entry.get()
        person_name = person_name_entry.get()
        roll_number = roll_number_entry.get()

        if not product_id.isdigit():
            messagebox.showwarning("Warning", "Please enter a valid Product ID.")
            return

        product_id = int(product_id)

        try:
            db = connect_db()
            cursor = db.cursor()

            # Check if the product exists
            cursor.execute("SELECT product_name, quantity FROM inventory WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()

            if result:
                product_name, quantity = result

                # Log the transaction before deleting the product
                log_transaction(product_id, quantity, 'delete', person_name, roll_number)
                cursor.execute("DELETE FROM inventory WHERE product_id = %s", (product_id,))
                db.commit()
                db.close()
                messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully.")
            else:
                db.close()
                messagebox.showwarning("Warning", "Product not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {e}")

    # UI
    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("500x400")
    delete_window.configure(bg=Theme.BG_DARK)

    tk.Label(delete_window, text="Delete Product", font=Theme.HEADER_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(pady=10)

    # Product ID Field
    product_id_frame = tk.Frame(delete_window, bg=Theme.BG_DARK)
    product_id_frame.pack(fill='x', pady=5, padx=20)

    tk.Label(product_id_frame, text="Product ID", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w')
    product_id_entry = ModernEntry(product_id_frame)
    product_id_entry.pack(fill='x', pady=5)

    # Person Name Field
    person_name_frame = tk.Frame(delete_window, bg=Theme.BG_DARK)
    person_name_frame.pack(fill='x', pady=5, padx=20)

    tk.Label(person_name_frame, text="Person Name", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w')
    person_name_entry = ModernEntry(person_name_frame)
    person_name_entry.pack(fill='x', pady=5)

    # Roll Number Field
    roll_number_frame = tk.Frame(delete_window, bg=Theme.BG_DARK)
    roll_number_frame.pack(fill='x', pady=5, padx=20)

    tk.Label(roll_number_frame, text="Roll Number", font=Theme.BODY_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(anchor='w')
    roll_number_entry = ModernEntry(roll_number_frame)
    roll_number_entry.pack(fill='x', pady=5)

    # Delete Button
    ModernButton(delete_window, text="Delete Product", command=delete_product).pack(pady=20)



def show_view_transactions():
    """View Transactions with enhanced UI."""
    try:
        window = tk.Toplevel()
        window.title("Transactions")
        window.geometry("1000x600")
        window.configure(bg=Theme.BG_DARK)

        tk.Label(window, text="Transactions", font=Theme.HEADER_FONT, fg=Theme.TEXT_PRIMARY, bg=Theme.BG_DARK).pack(pady=10)

        table_frame = tk.Frame(window, bg=Theme.BG_DARK)
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')

        tree = ttk.Treeview(table_frame, columns=("Transaction ID", "Product ID", "Name", "Quantity", "Type", "Person", "Roll"),
                            show="headings", yscrollcommand=scrollbar.set)
        tree.heading("Transaction ID", text="Transaction ID")
        tree.heading("Product ID", text="Product ID")
        tree.heading("Name", text="Product Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Type", text="Type")
        tree.heading("Person", text="Person Name")
        tree.heading("Roll", text="Roll Number")
        tree.pack(fill='both', expand=True)
        scrollbar.config(command=tree.yview)

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
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load transactions: {e}")


# Enhanced Login Window
def create_login_window():
    login_window = tk.Tk()
    login_window.title("Robotics Inventory Login")
    login_window.geometry("400x500")
    login_window.configure(bg=Theme.BG_DARK)

    # Center the login form
    frame = tk.Frame(login_window, bg=Theme.BG_DARK)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Logo/Header
    tk.Label(frame,
             text="🤖",  # Robot emoji as logo
             font=("Arial", 48),
             bg=Theme.BG_DARK,
             fg=Theme.TEXT_PRIMARY).pack(pady=(0, 20))

    tk.Label(frame,
             text="Robotics Inventory",
             font=Theme.HEADER_FONT,
             bg=Theme.BG_DARK,
             fg=Theme.TEXT_PRIMARY).pack()

    tk.Label(frame,
             text="Please login to continue",
             font=Theme.BODY_FONT,
             bg=Theme.BG_DARK,
             fg=Theme.TEXT_MUTED).pack(pady=(0, 30))

    # Username
    username_frame = tk.Frame(frame, bg=Theme.BG_DARK)
    username_frame.pack(fill='x', pady=10)

    tk.Label(username_frame,
             text="Username",
             font=Theme.BODY_FONT,
             bg=Theme.BG_DARK,
             fg=Theme.TEXT_PRIMARY).pack(anchor='w')

    username_entry = ModernEntry(username_frame)
    username_entry.pack(fill='x', pady=(5, 0))

    # Password
    password_frame = tk.Frame(frame, bg=Theme.BG_DARK)
    password_frame.pack(fill='x', pady=10)

    tk.Label(password_frame,
             text="Password",
             font=Theme.BODY_FONT,
             bg=Theme.BG_DARK,
             fg=Theme.TEXT_PRIMARY).pack(anchor='w')

    password_entry = ModernEntry(password_frame, show="●")
    password_entry.pack(fill='x', pady=(5, 0))

    # Login button
    login_btn = ModernButton(frame,
                             text="Login",
                             command=lambda: login(username_entry.get(),
                                                   password_entry.get(),
                                                   login_window))
    login_btn.pack(pady=30)

    return login_window


# Start the application
if __name__ == "__main__":
    apply_styles()
    login_window = create_login_window()
    login_window.mainloop()