CREATE DATABASE robotics_inventory;
USE robotics_inventory;


CREATE TABLE admin (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE,
            password_hash VARCHAR(255)
        );
        
INSERT INTO admin (username, password_hash) VALUES ("ratnesh", "Ratx100");
        
CREATE TABLE IF NOT EXISTS inventory (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) UNIQUE,
            quantity INT DEFAULT 0
        );

CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT PRIMARY KEY AUTO_INCREMENT,
            product_id INT,
            quantity INT,
            transaction_type ENUM('add', 'issue', 'delete'),
            person_name VARCHAR(100),
            roll_number VARCHAR(50),
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES inventory(product_id) ON DELETE CASCADE
        );
        
        