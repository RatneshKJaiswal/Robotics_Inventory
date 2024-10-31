import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import matplotlib.pyplot as plt

# Colors for a polished, dark theme
BG_COLOR = "#1f1f1f"
FG_COLOR = "#eaeaea"
ENTRY_BG = "#333333"
BTN_BG = "#3c3c3c"
BTN_FG = "#ffffff"
BTN_HOVER_BG = "#565656"
LIST_BG = "#2c2c2c"
LIST_ALT_BG = "#262626"
HIGHLIGHT_COLOR = "#00adb5"
HEADER_COLOR = "#323232"

HEADER_FONT = ("Poppins", 15, "bold")
LABEL_FONT = ("Poppins", 11)
ENTRY_FONT = ("Poppins", 11)
BUTTON_FONT = ("Poppins", 12, "bold")

# Database Connection Function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ratx100",
        database="robotics_inventory"
    )

# Improved Login UI
def show_login_ui():
    global username_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("1300x600")
    login_window.configure(bg=BG_COLOR)

    # Branding
    tk.Label(login_window, text="Robotics Inventory Management", bg=BG_COLOR, fg=HIGHLIGHT_COLOR,
             font=HEADER_FONT).pack(pady=20)

    # Username Entry
    tk.Label(login_window, text="Username:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    username_entry = tk.Entry(login_window, width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                              font=ENTRY_FONT)
    username_entry.pack(pady=10, padx=15, ipadx=5, ipady=5)

    # Password Entry
    tk.Label(login_window, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                              font=ENTRY_FONT)
    password_entry.pack(pady=10, padx=15, ipadx=5, ipady=5)

    # Login Button
    login_button = tk.Button(login_window, text="Login", command=login, bg=BTN_BG, fg=BTN_FG,
                             activebackground=BTN_HOVER_BG, font=BUTTON_FONT)
    login_button.pack(pady=20)

    login_window.mainloop()

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", "Welcome Admin!")
        login_window.destroy()
        inventory_portal()
    else:
        messagebox.showerror("Error", "Invalid credentials")

    cursor.close()
    db.close()

# Inventory Management Portal GUI
def inventory_portal():
    global product_name_entry, product_quantity_entry, inventory_tree, search_entry

    portal_window = tk.Tk()
    portal_window.title("Inventory Management Portal")
    portal_window.geometry("1300x600")
    portal_window.configure(bg=BG_COLOR)

    # Frames for better grouping
    input_frame = tk.Frame(portal_window, bg=BG_COLOR)
    input_frame.pack(pady=10)

    action_frame = tk.Frame(portal_window, bg=BG_COLOR)
    action_frame.pack(pady=10)

    inventory_frame = tk.Frame(portal_window, bg=BG_COLOR)
    inventory_frame.pack(pady=10)

    # Title and Entry Section
    tk.Label(input_frame, text="Product Name:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).grid(row=0, column=0,
                                                                                                padx=10, pady=5,
                                                                                                sticky="e")
    product_name_entry = tk.Entry(input_frame, width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                                  font=ENTRY_FONT)
    product_name_entry.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)

    tk.Label(input_frame, text="Quantity:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).grid(row=1, column=0, padx=10,
                                                                                            pady=5, sticky="e")
    product_quantity_entry = tk.Entry(input_frame, width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                                      font=ENTRY_FONT)
    product_quantity_entry.grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=5)

    tk.Label(input_frame, text="Search:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).grid(row=2, column=0, padx=10,
                                                                                          pady=5, sticky="e")
    search_entry = tk.Entry(input_frame, width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, font=ENTRY_FONT)
    search_entry.grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)

    search_button = tk.Button(input_frame, text="Search", command=lambda: show_inventory(search_entry.get().strip()),
                              width=10, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_HOVER_BG, font=BUTTON_FONT,
                              relief="flat")
    search_button.grid(row=2, column=2, padx=10, pady=5)

    # Styled Buttons
    add_button = tk.Button(action_frame, text="Add / Update Product", command=add_or_update_product, width=20,
                           bg=BTN_BG, fg=BTN_FG, activebackground=BTN_HOVER_BG, font=BUTTON_FONT, relief="flat")
    add_button.grid(row=0, column=0, padx=10, pady=5)

    issue_button = tk.Button(action_frame, text="Issue Product", command=issue_product, width=20, bg=BTN_BG, fg=BTN_FG,
                             activebackground=BTN_HOVER_BG, font=BUTTON_FONT, relief="flat")
    issue_button.grid(row=0, column=1, padx=10, pady=5)

    delete_button = tk.Button(action_frame, text="Delete Product", command=delete_product, width=20, bg=BTN_BG,
                              fg=BTN_FG, activebackground=BTN_HOVER_BG, font=BUTTON_FONT, relief="flat")
    delete_button.grid(row=0, column=2, padx=10, pady=5)

    # Inventory Display Section
    tk.Label(inventory_frame, text="Current Available Inventory", bg=BG_COLOR, fg=HIGHLIGHT_COLOR,
             font=HEADER_FONT).pack(pady=20)

    # Treeview for Inventory List
    columns = ('Product Name', 'Quantity')
    inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=13)
    inventory_tree.heading('Product Name', text='Product Name')
    inventory_tree.heading('Quantity', text='Quantity')

    # Set column widths to increase table width
    inventory_tree.column('Product Name', width=500, anchor="center")  # Increased width for product name
    inventory_tree.column('Quantity', width=130, anchor="center")  # Increased width for quantity

    # Treeview Style
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=LIST_BG,
                    foreground=FG_COLOR,
                    rowheight=45,
                    fieldbackground=LIST_BG,
                    font=LABEL_FONT)
    style.configure("Treeview.Heading",
                    font=BUTTON_FONT,
                    rowheight=45,
                    foreground=FG_COLOR,
                    background=HEADER_COLOR)
    style.map("Treeview",
              background=[('selected', HIGHLIGHT_COLOR)],
              foreground=[('selected', FG_COLOR)])

    inventory_tree.tag_configure('evenrow', background=LIST_BG)
    inventory_tree.tag_configure('oddrow', background=LIST_ALT_BG)

    inventory_tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    show_inventory()
    portal_window.mainloop()

# Display Inventory with Enhanced Appearance
def show_inventory(search_term=""):
    for item in inventory_tree.get_children():
        inventory_tree.delete(item)

    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM inventory WHERE product_name LIKE %s ORDER BY product_name ASC"
    cursor.execute(query, (f"%{search_term}%",))
    rows = cursor.fetchall()

    for i, (id, product_name, quantity) in enumerate(rows):
        bg_color = LIST_BG if i % 2 == 0 else LIST_ALT_BG
        inventory_tree.insert("", "end", values=(product_name, quantity), tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    cursor.close()
    db.close()

# Add or Update Product
def add_or_update_product():
    name = product_name_entry.get().strip()
    quantity = product_quantity_entry.get().strip()

    if not name or not quantity.isdigit():
        messagebox.showerror("Error", "Please enter a valid product name and quantity.")
        return

    quantity = int(quantity)

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT quantity FROM inventory WHERE product_name=%s", (name,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE inventory SET quantity = quantity + %s WHERE product_name = %s", (quantity, name))
        messagebox.showinfo("Updated", f"Updated '{name}' quantity by {quantity}.")
    else:
        cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)", (name, quantity))
        messagebox.showinfo("Added", f"Added new product '{name}' with quantity {quantity}.")

    db.commit()
    cursor.close()
    db.close()
    show_inventory()


# Delete Product Function
def delete_product():
    selected_item = inventory_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No product selected for deletion.")
        return

    product_name = inventory_tree.item(selected_item, 'values')[0]

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM inventory WHERE product_name=%s", (product_name,))
    db.commit()

    messagebox.showinfo("Deleted", f"Product '{product_name}' has been deleted from the inventory.")

    cursor.close()
    db.close()
    show_inventory()


# Issue Product Function
def issue_product():
    name = product_name_entry.get().strip()
    quantity = product_quantity_entry.get().strip()

    if not name or not quantity.isdigit():
        messagebox.showerror("Error", "Please enter a valid product name and quantity.")
        return

    quantity = int(quantity)

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT quantity FROM inventory WHERE product_name=%s", (name,))
    result = cursor.fetchone()

    if result and result[0] >= quantity:
        cursor.execute("UPDATE inventory SET quantity = quantity - %s WHERE product_name = %s", (quantity, name))
        db.commit()
        messagebox.showinfo("Success", f"Issued {quantity} of '{name}'.")
    else:
        messagebox.showerror("Error", "Insufficient quantity or product not found.")

    cursor.close()
    db.close()
    show_inventory()

# Run the application
show_login_ui()
