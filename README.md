Steps Overview:

Database Setup: Create an inventory database and an admin table to store the login credentials.
GUI Setup: Use tkinter to create the login page and inventory management sections (Add Product, Issue Product, View Inventory).
MySQL Connection: Connect to the database to execute SQL queries based on GUI inputs.

Automatic Quantity Updates: When adding an existing product, the code now automatically increases the quantity without requiring user confirmation or complex handling.
Field Validation: Checks for valid inputs before proceeding with database operations, reducing errors and improving usability.
Alphabetically Sorted Inventory Display: show_inventory() arranges the products alphabetically, making it easier for the admin to locate specific items in the list.
