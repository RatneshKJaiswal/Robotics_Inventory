CREATE DATABASE robotics_inventory;
USE robotics_inventory;

-- Create the admin table to store login credentials
CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
);

-- Insert a default admin user (replace 'admin_password' with a secure password)
INSERT INTO admin (username, password) VALUES ('ratnesh', 'Ratx100');

-- Create the inventory table
CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT DEFAULT 0
);

-- Create the transactions table to store past operations on inventory items
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    product_name VARCHAR(100),
    quantity INT,
    transaction_type ENUM('add', 'issue', 'delete'),
    person_name VARCHAR(100),
    roll_number VARCHAR(50),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES inventory(product_id)
);