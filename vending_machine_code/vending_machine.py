import sqlite3
import os

# Product class represents a product in the vending machine
class Product:
    def __init__(self, id, name, price, stock, db_name='shop.db'):
        self.id = id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.db_name = db_name

    def update_stock(self, quantity):
        """Reduce stock in both object and database."""
        self.stock -= quantity
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "UPDATE Products SET Stock = ? WHERE productID = ?"
        cursor.execute(query, (self.stock, self.id))
        conn.commit()
        conn.close()

    def restock(self, quantity):
        """ Increasing stock in both object and database. """
        self.stock += quantity
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "UPDATE Products SET Stock = ? WHERE productID = ?"
        cursor.execute(query, (self.stock, self.id))
        conn.commit()
        conn.close()

    def __str__(self):
        """String representation of product for display"""
        return f"{self.id}: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}"


# Cart class manages a user's shopping cart
class Cart:
    def __init__(self):
        # Initialize an empty dictionary to hold cart items
        self.items = {}

    # Method to add a product to the cart
    def add_item(self, product, quantity):
        if quantity > 0:  # Check for positive quantity
            quantity = int(quantity)
            if product.stock >= quantity:
                # If product not already in cart, add it with quantity
                if product.id not in self.items:
                    self.items[product.id] = {'product': product, 'quantity': quantity}
                else:
                    # If product already in cart, increase quantity
                    self.items[product.id]['quantity'] += quantity
                product.update_stock(quantity)
                print(f"Added {quantity} x {product.name} to cart.")
            else:
                print(f"Not enough stock for {product.name}.")
        else:
            print(f"Cannot add {quantity} x {product.name}.")

    def remove_item(self, product, quantity):
        """Remove product from cart with specified quantity"""
        quantity = int(quantity)
        if quantity > 0:  # Only allow positive quantities
            if product.id in self.items:
                # Item exists in cart
                cart_quantity = self.items[product.id]['quantity']
                # Remove all
                if quantity >= cart_quantity:
                    removed_quantity = cart_quantity
                    self.items.pop(product.id)
                    product.restock(removed_quantity)
                    print(f"Removed all {removed_quantity} x {product.name} from cart.")
                else:
                    # Remove partial quantity
                    removed_quantity = quantity
                    self.items[product.id]['quantity'] -= removed_quantity
                    product.restock(removed_quantity)
                    print(f"Removed {removed_quantity} x {product.name} from cart.")
                return removed_quantity
            else:
                print(f"{product.name} is not in your cart.")
        else:
            print(f"Cannot remove {quantity} x {product.name}.")
        return 0

    def view_items(self):
        """Display all items in cart with total price"""
        if not self.items:
            print("Your cart is empty.")
            return
        print("\nYour cart:")
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            print(f"{product.name} | Quantity: {quantity} | Price per item: ${product.price:.2f}")
        print(f"Total: ${self.calculate_total():.2f}")

    def calculate_total(self):
        """Calculate total price of all items in cart"""
        return sum(item['product'].price * item['quantity'] for item in self.items.values())

    def clear_cart(self):
        """Empty the cart completely"""
        self.items.clear()


# SmartVendingMachine class manages the vending machine's inventory and operations
class SmartVendingMachine:
    def __init__(self, db_name='shop.db'):
        """Initialize vending machine with database name"""
        self.db_name = db_name

    def initialise_database(self, sql_file="shop.sql"):
        """Initialize the database by running the SQL script."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        with open(sql_file, "r") as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()

    def get_all_products(self):
        """Retrieve all products from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "SELECT * FROM Products"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        products = []
        for row in rows:
            product_info= {
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'stock': row[3],
            }
            products.append(product_info)
        return products

    def register_user(self, username, password):
        """Register new user with username and password"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Check if username exists
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists. Please try again."

        # Create new user
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True, "User registered successfully. You can log in."

    def login_user(self, username, password):
        """Authenticate user with username and password"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Debug print to see what's being compared
            print(f"Login attempt - Username: {username}, Password: {password}")

            # Check credentials
            cursor.execute("SELECT userID FROM Users WHERE username = ? AND password = ?",
                           (username, password))
            row = cursor.fetchone()

            # Debug print to see query result
            print("Database returned:", row)

            if row:  # Successful login
                return True, "Login successful.", row[0]
            else:
                # Check if username exists at all
                cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return False, "Incorrect password.", None  # Username exists but wrong password
                else:
                    return False, "Username not found.", None  # Username doesn't exist
        except sqlite3.Error as e:
            print("Database error:", str(e))
            return False, "Database error during login.", None
        finally:
            conn.close()

    def find_product_by_id(self, product_id):
        """Find product by its ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "SELECT * FROM Products WHERE productID = ?"
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(row[0], row[1], row[2], row[3], self.db_name)
        else:
            return None

    def save_transaction(self, user_id, product_id, quantity, total_price, payment_method):
        """Method to save completed transaction details to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "INSERT INTO CartTransactions(userID, productID,\
quantity, total_price, payment_method) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (user_id, product_id, quantity, total_price, payment_method))
        conn.commit()
        conn.close()
        print("Transaction has been recorded.")

    def analyse_sold_products(self):
        """Analyze sales data by product"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Name table Product as p and table CartTransactions as c
        query = """
               SELECT p.productID, SUM(c.quantity) AS total_sold
               FROM CartTransactions c
               JOIN Products p ON c.productID = p.productID
               GROUP BY p.productID
               ORDER BY total_sold DESC
           """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def product_sales(self):
        """Get sales data by product per user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Get quantity sold per product per user
        query = """
                    SELECT 
                        p.ProductName,
                        t.userID,
                        SUM(t.quantity) as total_quantity
                    FROM CartTransactions t
                    JOIN Products p ON t.productID = p.productID
                    GROUP BY p.ProductName, t.userID
                    ORDER BY t.userID, p.ProductName
                """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def checkout(self, cart, payment_method):
        """Process cart checkout"""
        cart.view_items()
        # If cart is empty
        if not cart.items:
            print("\nYour cart is empty. Nothing to checkout.")
            return

        # Enter confirmation choice
        confirm = input("\nDo you want to proceed with the purchase? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            # Save transaction
            for item in cart.items.values():
                product = item['product']
                quantity = item['quantity']
                total_price = product.price * quantity
                self.save_transaction(product.id, quantity, total_price, payment_method)
            cart.clear_cart()
            print("\nPurchase confirmed. Thank you for shopping with us.")
        elif confirm in ['no', 'n']:
            print("\nCheckout cancelled.")
        else:
            print("\nInvalid input.")

    @staticmethod
    # Does not form part of SmartVendingMachine class
    def restore_cart_to_database(cart):
        """Restores all items in the given cart back to database"""
        for item in cart.items.values():
            product = item['product']
            quantity = item['quantity']
            product.restock(quantity)
        cart.clear_cart()
        print("Cart contents restored to database.")

    def menu(self, payment_method):
        """Display main menu and handle user interactions"""
        cart = Cart()
        print("\n***** Welcome to the Smart Vending Machine! *****")
        while True:
            print("\nPlease choose an option:")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.get_all_products()
            elif choice == '2':
                product_id = input("Enter Product ID: ")
                product = self.find_product_by_id(product_id)
                if product:
                    quantity = input("Enter quantity: ")
                    cart.add_item(product, quantity)
                else:
                    print("Product not found.")
            elif choice == '3':
                product_id = input("Enter Product ID: ")
                product = self.find_product_by_id(product_id)
                if product:
                    quantity = input("Enter quantity to remove: ")
                    cart.remove_item(product, quantity)
                else:
                    print("Product not found.")
            elif choice == '4':
                cart.view_items()
            elif choice == '5':
                smart_vending_machine.checkout(cart, payment_method)
            elif choice == '6':
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice.")

# Create and run vending machine
smart_vending_machine = SmartVendingMachine()

# Initialize database if it doesn't exist
if not os.path.exists('shop.db'):
    smart_vending_machine.initialise_database("shop.sql")
    print("Database created and initialised.")
else:
    print("Database found.")


