import socket
import pickle
from vending_machine import SmartVendingMachine, Cart

# Server connection settings
HOST = "localhost"
PORT = 5050
ADDRESS = (HOST, PORT)
BUF_SIZE = 4096

# Create SmartVendingMachine instance
smart_vending_machine = SmartVendingMachine()

def handle_register(client, username, password):
    """Handle user registration request"""
    try:
        success, message = smart_vending_machine.register_user(username, password)
        response = {
            "status": "success" if success else "error",
            "message": message
        }
        # Send feedback to client
        client.sendall(pickle.dumps(response))
    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Registration error: {str(e)}"
        }
        client.sendall(pickle.dumps(error_response))

def handle_login(client, username, password):
    """Handle login request and return user ID if successful"""
    try:
        success, message, user_id = smart_vending_machine.login_user(username, password)
        response = {
            "status": "success" if success else "error",
            "message": message,
            "user_id": user_id
        }
        client.sendall(pickle.dumps(response))
        # Only return user ID if login passed
        return user_id if success else None
    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Login error: {str(e)}",
            "user_id": None
        }
        client.sendall(pickle.dumps(error_response))
        return None

def handle_view_products(client):
    """Send list of products to the client"""
    products = smart_vending_machine.get_all_products()
    client.sendall(pickle.dumps(products))

def handle_add_to_cart(client, cart, product_id, quantity):
    """Add a product to the user's cart if stock is available"""
    product = smart_vending_machine.find_product_by_id(product_id)
    if quantity > 0:
        if product:
            if product.stock >= quantity:
                cart.add_item(product, quantity)
                response = f"Added {quantity} x {product.name} to your cart."
            else:
                response = f"Not enough stock for {product.name}."
        else:
            response = "Product not found."
    else:
        response = "Cannot add 0 items."
    client.sendall(pickle.dumps(response))

def handle_remove_from_cart(client, cart, product_id, removed_quantity):
    """Remove a quantity of an item from the user's cart"""
    product = smart_vending_machine.find_product_by_id(product_id)
    if removed_quantity > 0:
        if product:
            if product.id in cart.items:
                removed_quantity = cart.remove_item(product, removed_quantity)
                response = f"Removed {removed_quantity} x {product.name} from your cart."
            else:
                response = f"{product.name} is not in your cart."
        else:
            response = "Product not found."
    else:
        response = "Cannot remove 0 items."
    client.sendall(pickle.dumps(response))

def handle_view_cart(client, cart):
    """Send the current contents of the user's cart to the client"""
    if not cart.items:
        client.sendall(pickle.dumps("Your cart is empty."))
        return

    cart_list = []
    for item in cart.items.values():
        product = item['product']
        quantity = item['quantity']
        total_price = product.price * quantity
        cart_list.append({
            'id': product.id,
            'name': product.name,
            'quantity': quantity,
            'price': product.price,
            'total': total_price
        })
    total_price = cart.calculate_total()
    response = {
        "items": cart_list,
        "total_amount": total_price
    }
    client.sendall(pickle.dumps(response))

def handle_analytics(client):
    """Send product analytics data (total sold quantities) to the client"""
    results = smart_vending_machine.analyse_sold_products()
    client.sendall(pickle.dumps(results))

def handle_product_trends(client):
    """Send sales trends (by product and user) data for plotting to the client"""
    try:
        results = smart_vending_machine.product_sales()
        if not results:
            return client.sendall(pickle.dumps({
                "status": "empty",
                "message": "No transaction data found"
            }))

        # Structure: {product: {user_id: total_quantity}}
        trends_data = {}
        product_names = set()
        user_ids = set()

        for product, user_id, quantity in results:
            product_names.add(product)
            user_ids.add(user_id)
            if product not in trends_data:
                trends_data[product] = {}
            trends_data[product][user_id] = quantity

        # Convert to list for ordered plotting
        sorted_users = sorted(user_ids)
        sorted_products = sorted(product_names)

        # Prepare plot data
        plot_data = {
            "user_ids": sorted_users,
            "products": sorted_products,
            "quantities": [
                [trends_data[product].get(user, 0) for user in sorted_users]
                for product in sorted_products
            ]
        }

        client.sendall(pickle.dumps({
            "status": "success",
            "data": plot_data
        }))
        return None

    except Exception as e:
        client.sendall(pickle.dumps({
            "status": "error",
            "message": f"Error generating trends: {str(e)}"
        }))
        return None

def handle_checkout(client, cart, user_id):
    """Process cart checkout, record transactions, and manage payment selection"""
    if not user_id:
        client.sendall(pickle.dumps("Error: User not authenticated."))
        return
    if not cart.items:
        client.sendall(pickle.dumps("Your cart is empty. Nothing to checkout."))
        return

    client.sendall(pickle.dumps("Do you want to proceed with the purchase?"))
    confirmation = pickle.loads(client.recv(BUF_SIZE)).lower()

    if confirmation in ["yes", "y"]:
        # Payment selection prompt
        payment_msg = (
            "\nSelect a payment method:\n"
            "1. Credit Card\n"
            "2. Debit Card\n"
            "3. Cash\n"
            "Enter your choice:"
        )
        client.sendall(pickle.dumps(payment_msg))
        choice = pickle.loads(client.recv(BUF_SIZE))

        # Identify payment method based on choice
        if choice == '1':
            payment_method = "Credit Card"
        elif choice == '2':
            payment_method = "Debit Card"
        elif choice == '3':
            payment_method = "Cash"
        else:
            client.sendall(pickle.dumps("Invalid payment method. Transaction cancelled."))
            return

        # Save each item in the transaction table and clear cart
        for item in cart.items.values():
            product = item['product']
            quantity = item['quantity']
            total_price = product.price * quantity
            smart_vending_machine.save_transaction(user_id, product.id, quantity, total_price, payment_method)
        cart.clear_cart()
        client.sendall(pickle.dumps(f"Purchase confirmed via {payment_method}. Thank you for shopping with us!"))

    elif confirmation in ["no", "n"]:
        client.sendall(pickle.dumps("Checkout cancelled."))

    else:
        client.sendall(pickle.dumps("Invalid choice. Please enter yes or no."))

"""Handle client disconnection; return cart items to inventory if any"""
def handle_exit(client, cart):
    if cart.items:
        smart_vending_machine.restore_cart_to_database(cart)
        client.sendall(pickle.dumps("Cart restored to inventory. Disconnected."))
        print("Client disconnected. Items returned to inventory.")
    else:
        client.sendall(pickle.dumps("Disconnected from server."))
        print("Client disconnected.")

def handle_client(client):
    cart = Cart()   # each client has its own cart
    user_id = None   # user ID for authenticated actions

    while True:
        try:
            request = client.recv(BUF_SIZE).decode()
            if not request:
                break

            if user_id is None:
                # User must register or login first
                if request.startswith("REGISTER"):
                    _, username, password = request.split(",", 2)
                    handle_register(client, username, password)

                elif request.startswith("LOGIN"):
                    _, username, password = request.split(",", 2)
                    user_id = handle_login(client, username, password)
                    if not user_id:
                        # Login failed; user_id stays None
                        continue
                    else:
                        # Optionally send welcome message here
                        pass

                else:
                    client.sendall(pickle.dumps("Please login or register first."))

            else:
                # If authenticated, handle client requests
                if request.startswith("VIEW"):
                    handle_view_products(client)

                elif request.startswith("ADD"):
                    _, product_id, quantity = request.split(",")
                    handle_add_to_cart(client, cart, product_id, int(quantity))

                elif request.startswith("REMOVE"):
                    _, product_id, quantity = request.split(",")
                    handle_remove_from_cart(client, cart, product_id, int(quantity))

                elif request.startswith("CART"):
                    handle_view_cart(client, cart)

                elif request.startswith("CHECKOUT"):
                    handle_checkout(client, cart, user_id)

                elif request.startswith("ANALYTICS"):
                    handle_analytics(client)

                elif request == "PRODUCT_TRENDS":
                    handle_product_trends(client)

                elif request.startswith("EXIT"):
                    handle_exit(client, cart)
                    break

                else:
                    client.sendall(pickle.dumps("Unknown command."))

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            client.sendall(pickle.dumps(error_msg))

    client.close()

def main():
    """Start the TCP server and accept client connections"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(5)
    print("Server running. Waiting for connections...")

    while True:
        client, address = server.accept()
        print(f"Connected to {address}")
        welcome_msg = "Hello client, you are now connected to the vending machine server."
        client.send(welcome_msg.encode())
        handle_client(client)

if __name__ == "__main__":
    main()
