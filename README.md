# Robotics Inventory Management System

This project is a GUI-based Inventory Management System developed with Python's `tkinter` library for graphical interfaces and MySQL for database management. The system provides functionalities for managing products, such as adding new items, issuing products, and viewing inventory details. It includes user authentication and automated inventory updates to streamline product handling.

## Features

1. **Database Setup**: 
   - A MySQL database stores all inventory data and user login credentials.
   - Inventory records are maintained for easy access and management.
   
2. **GUI Setup**:
   - The GUI is built using `tkinter`, with separate sections for:
     - **Login Page**: Secure access for authorized users.
     - **Inventory Management**: Includes pages for adding products, issuing products, and viewing the complete inventory.
   
3. **MySQL Connection**:
   - The system connects to MySQL to execute queries based on inputs from the GUI, allowing seamless database interaction.
   
4. **Automatic Quantity Updates**:
   - When adding an existing product, the system automatically updates the quantity. This simplifies inventory handling and reduces redundant steps.

5. **Field Validation**:
   - Ensures valid data entry before executing database operations, reducing errors and improving user experience.
   
6. **Alphabetically Sorted Inventory Display**:
   - The `show_inventory()` function displays products in alphabetical order, making it easier for the admin to locate specific items.

## Requirements

- Python 3.x
- Tkinter (included with standard Python installation)
- MySQL
- MySQL Connector for Python

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RatneshKJaiswal/Robotics_Inventory


# Project Gallery

