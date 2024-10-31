CREATE DATABASE robotics_inventory;
USE robotics_inventory;

-- Create the admin table to store login credentials
CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
);

-- Insert a default admin user (replace 'admin_password' with a secure password)
INSERT INTO admin (username, password) VALUES ('admin', 'admin_password');

-- Create the inventory table
CREATE TABLE inventory (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    quantity INT DEFAULT 0
);