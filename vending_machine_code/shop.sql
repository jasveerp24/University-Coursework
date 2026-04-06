-- Create the Products table
CREATE TABLE IF NOT EXISTS Products (
    productID INTEGER PRIMARY KEY,
    ProductName TEXT NOT NULL,
    Price DECIMAL(4,2) NOT NULL,
    Stock INTEGER NOT NULL
);

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Create the CartTransactions table
CREATE TABLE IF NOT EXISTS CartTransactions (
    transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    productID INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price DECIMAL(4,2) NOT NULL,
    payment_method TEXT NOT NULL,
    transactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (productID) REFERENCES Products(productID)
);


-- Insert or update data into Products table
INSERT INTO Products (productID, ProductName, Price, Stock) VALUES
    (1, "E-Book: Python for Beginners", 12.99, 50),
    (2, "Audio Book: Mindful Productivity", 9.99, 50),
    (3, "Music Album: Chill Beats", 7.50, 50),
    (4, "Video Course: Web Development", 25.00, 50),
    (5, "Software License: PhotoPro X", 49.99, 50),
    (6, "Software License: SecureShield VPN", 29.95, 50)

