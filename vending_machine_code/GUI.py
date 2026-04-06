import pickle
import socket
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants
HOST = "localhost"
PORT = 5050
ADDRESS = (HOST, PORT)
BUF_SIZE = 4096

# Client Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
recv_msg = client.recv(BUF_SIZE)
print(recv_msg.decode())

# Main Window Setup
root = Tk()
root.title("Shopping System")

# Centering the window at the middle of my screen
window_width = 990
window_height = 610
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width / 2) - window_width / 2)
center_y = int((screen_height / 2) - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Set window icon
root.iconbitmap(r"logo.ico")

# Frame variable
login_frame = None
register_frame = None

# Frames setup
welcome_frame = LabelFrame(root,
                           text="Smart Vending Machine",
                           font=("Arial", 12, "bold"),
                           bg="white",
                           padx=5, pady=5,
                           width=300, height=500)

main_frame = LabelFrame(root,
                        text="Digital Products",
                        font=("Arial", 12, "bold"),
                        bg="light blue",
                        padx=10, pady=10)

top_frame = Frame(root, bg="light grey")

analytics_frame = LabelFrame(root,
                             text="📊 Sales Analytics",
                             font=("Arial", 12, "bold"),
                             bg="light blue",
                             padx=10, pady=10,
                             width=300, height=500)

cart_frame = LabelFrame(root,
                        text="Your Cart 🛒",
                        font=("Arial", 12, "bold"),
                        bg="light blue",
                        padx=10, pady=10,
                        width=300, height=500)

sales_trend_frame = LabelFrame(root,
                               text="📈 Sales Trends",
                               font=("Arial", 12, "bold"),
                               bg="light blue",
                               padx=10, pady=10,
                               width=380, height=500)

# Placeholders for cart components
product_id_entry = None
quantity_entry = None
cart_text = None

def set_up_main():
    """Set up the main system interface after login"""
    # Top control bar
    top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

    # Products
    main_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    # Welcome message
    welcome_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")

    # Configure the grid layout for the top_frame:
    top_frame.grid_columnconfigure(1, weight=0)     # Column 1: no extra space
    top_frame.grid_columnconfigure(2, weight=1)     # Column 2: expands to fill available horizontal space
    top_frame.grid_columnconfigure(3, weight=0)     # Column 3: no extra space
    top_frame.grid_columnconfigure(4, weight=0)     # Column 4: no extra space


def show_login():
    """Display the login screen"""
    global login_frame, register_frame

    # Clear any existing frames
    if register_frame:
        register_frame.destroy()
    if login_frame:
        login_frame.destroy()

    # Create login frame
    login_frame = Frame(root, padx=5, pady=5)
    login_frame.pack(expand=True)

    Label(login_frame,
          text="Login to Smart Vending Machine",
          font=("Arial", 13, "bold")
          ).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    # Username label + entry field
    Label(login_frame, text="Username: ").grid(row=1, column=0, sticky=E)
    username_entry = Entry(login_frame)
    username_entry.grid(row=1, column=1)

    # Password label + entry field (with password masking)
    Label(login_frame, text="Password: ").grid(row=2, column=0, sticky=E)
    password_entry = Entry(login_frame, show="*")
    password_entry.grid(row=2, column=1)

    # Label for displaying error or feedback messages
    message_label = Label(login_frame, text="", fg="red")
    message_label.grid(row=3, column=0, columnspan=2)

    def handle_login():
        """Handles login form submission"""

        # Fetch values from input fields
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Check for empty entries
        if not (username and password):
            message_label.config(text="Please enter both username and password.")
            return

        try:
            # Send login message to server
            message = f"LOGIN,{username},{password}"
            client.sendall(message.encode())

            # Receive and unpickle response
            response_data = client.recv(BUF_SIZE)
            response = pickle.loads(response_data)

            # Print to see actual server response
            print("Server login response:", response)

            # Handle response
            if isinstance(response, dict):
                if response.get("status") == "success":
                    # Successful login: clear login screen, show main system
                    message_label.config(text="")
                    login_frame.destroy()
                    set_up_main()
                    view_products()
                else:
                    # Display server-provided error message
                    error_msg = response.get("message", "Login failed. Invalid credentials.")
                    message_label.config(text=error_msg)
            else:
                message_label.config(text="Invalid server response format")

        # Handle pickle or network errors gracefully
        except pickle.PickleError:
            message_label.config(text="Communication error with server.")
        except Exception as e:
            message_label.config(text=f"Login error: {str(e)}")

    # Login and Register buttons
    Button(login_frame, text="Login",
           width=10,
           command=handle_login
           ).grid(row=4, column=0, padx=5, pady=5)

    Button(login_frame,
           text="Register",
           width=10,
           command=show_register
           ).grid(row=4, column=1, padx=5, pady=5)

def show_register():
    """Display the register screen"""
    global register_frame, login_frame

    # Clear any existing frames
    if login_frame:
        login_frame.destroy()
    if register_frame:
        register_frame.destroy()
    # Create new register frame inside root window
    register_frame = Frame(root, padx=5, pady=5)
    register_frame.pack(expand=True)

    # Title label
    Label(register_frame,
          text="Register New Account",
          font=("Arial", 13, "bold")
          ).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    # Username input
    Label(register_frame, text="Username: ").grid(row=1, column=0, sticky=E)
    reg_username_entry = Entry(register_frame)
    reg_username_entry.grid(row=1, column=1)

    # Password input
    Label(register_frame, text="Password: ").grid(row=2, column=0, sticky=E)
    reg_password_entry = Entry(register_frame, show="*")
    reg_password_entry.grid(row=2, column=1)

    # Confirm password input
    Label(register_frame, text="Confirm Password: ").grid(row=3, column=0, sticky=E)
    reg_confirm_password_entry = Entry(register_frame, show="*")
    reg_confirm_password_entry.grid(row=3, column=1)

    # Message label to display validation errors or server messages
    message_label = Label(register_frame, text="", fg="red")
    message_label.grid(row=4, column=0, columnspan=2)

    def handle_register():
        """Handles register form submission"""
        # Fetch values from input fields
        username = reg_username_entry.get().strip()
        password = reg_password_entry.get().strip()
        confirm_password = reg_confirm_password_entry.get().strip()

        # Input validation
        if not (username and password and confirm_password):
            message_label.config(text="All fields are required.")
            return
        if password != confirm_password:
            message_label.config(text="Passwords don't match.")
            return
        if len(username) < 4 or len(password) < 4:
            message_label.config(text="Username and password must be at least 4 characters.")
            return

        try:
            # Send register message to server
            message = f"REGISTER,{username},{password}"
            client.sendall(message.encode())

            # Receive and unpickle response
            response_data = client.recv(BUF_SIZE)
            response = pickle.loads(response_data)

            # Handle response
            if isinstance(response, dict):
                # If registration is successful
                if response.get("status") == "success":
                    # Show success messagebox with server-provided message
                    messagebox.showinfo("Success", response.get("message", "Registration successful!"))

                    # Remove register frame and display login screen again
                    register_frame.destroy()
                    show_login()
                else:
                    # If registration failed, show error message from server
                    message_label.config(text=response.get("message", "Registration failed."))
            else:
                # If unexpected server response (not a dictionary)
                message_label.config(text="Unexpected server response.")

        # Handle pickle or communication errors gracefully
        except pickle.PickleError:
            message_label.config(text="Communication error with server.")
        except Exception as e:
            message_label.config(text=f"Error: {str(e)}")

    # Register and Back to log in buttons
    Button(register_frame, text="Register", width=10, command=handle_register).grid(row=5, column=0, padx=5, pady=5)
    Button(register_frame, text="Back to Login", width=10, command=show_login).grid(row=5, column=1, padx=5, pady=5)

def show_welcome_frame():
    """Shows the welcome frame and hides others"""
    if cart_frame.winfo_ismapped():
        cart_frame.grid_remove()
    if analytics_frame.winfo_ismapped():
        analytics_frame.grid_remove()
    if sales_trend_frame.winfo_ismapped():
        sales_trend_frame.grid_remove()
    welcome_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")

def toggle_cart_frame():
    """Toggles the shopping cart frame visibility"""
    # Hide other frames first
    if analytics_frame.winfo_ismapped():
        analytics_frame.grid_remove()
    if welcome_frame.winfo_ismapped():
        welcome_frame.grid_remove()
    if sales_trend_frame.winfo_ismapped():
        sales_trend_frame.grid_remove()
    if cart_frame.winfo_ismapped():
        cart_frame.grid_remove()
    else:
        cart_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")
        view_cart()  # Refresh cart contents

def toggle_analytics_frame():
    if cart_frame.winfo_ismapped():
        cart_frame.grid_remove()
    if welcome_frame.winfo_ismapped():
        welcome_frame.grid_remove()
    if sales_trend_frame.winfo_ismapped():
        sales_trend_frame.grid_remove()
    if analytics_frame.winfo_ismapped():
        analytics_frame.grid_remove()
    else:
        show_analytics_chart()
        analytics_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")

def toggle_sales_trend_frame():
    if cart_frame.winfo_ismapped():
        cart_frame.grid_remove()
    if analytics_frame.winfo_ismapped():
        analytics_frame.grid_remove()
    if welcome_frame.winfo_ismapped():
        welcome_frame.grid_remove()
    if sales_trend_frame.winfo_ismapped():
        sales_trend_frame.grid_remove()
    else:
        show_sales_trends()
        sales_trend_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")

def view_products():
    """Fetch and display products from server in a grid layout"""
    client.sendall("VIEW".encode())
    data = client.recv(BUF_SIZE)
    products = pickle.loads(data)

    for widget in main_frame.winfo_children():
        widget.destroy()

    # If no products were returned
    if not products:
        Label(main_frame, text="No products available", font=("Arial", 12)).pack()
        return

    products_grid = Frame(main_frame)
    products_grid.pack(padx=10, pady=10)

    # Display the products in a 3x2 table
    for i, product in enumerate(products):
        row = i // 2
        col = i % 2

        # Creating and placing product_frame with some labels
        product_frame = Frame(products_grid, bd=2, relief=GROOVE, padx=5, pady=5)
        product_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        Label(product_frame, text=f"Id: {product['id']}", font=("Arial", 9)).pack()
        Label(product_frame, text=product['name'], font=("Arial", 10, "bold")).pack()
        Label(product_frame, text=f"${product['price']:.2f}", font=("Arial", 9)).pack()
        Label(product_frame, text=f"Stock: {product['stock']}", font=("Arial", 9)).pack()

        # 'Add to Cart' button — when clicked, reveals the quantity entry field for this product
        Button(product_frame,
               text="Add to Cart",
               bg="green",
               fg="white",
               font=("Arial", 8, "bold"),
               command=lambda p=product: show_quantity_entered(p)).pack(pady=5)
                # lambda is used so that execution is delayed when button is clicked

        # Frame to hold quantity input and Add button — initially hidden until 'Add to Cart' is clicked
        quantity_frame = Frame(product_frame)
        Label(quantity_frame, text="Qty:", font=("Arial", 8)).pack(side=LEFT)

        quantity_entered = Entry(quantity_frame, width=5)
        quantity_entered.pack(side=LEFT, padx=5)

        # Button to confirm adding specified quantity to cart
        Button(quantity_frame,
               text="Add",
               bg="blue",
               fg="white",
               font=("Arial", 8),
               command=lambda p=product, e=quantity_entered: add_item(p, e)
               ).pack(side=LEFT)

        # Attach the quantity_frame to the product dictionary for later reference when toggling it
        product['quantity_frame'] = quantity_frame

def show_quantity_entered(product):
    """Show quantity entry for a specific product"""
    if product['quantity_frame'].winfo_ismapped():
        product['quantity_frame'].pack_forget()
    else:
        # Hide all other quantity frames inside product frames
        for child in main_frame.winfo_children():
            for product_frame in child.winfo_children():
                for widget in product_frame.winfo_children():
                    if isinstance(widget, Frame):
                        widget.pack_forget()

        # Show the selected one
        product['quantity_frame'].pack()


def add_item(product, quantity_entered):
    """Add a product to cart with given quantity"""

    # Get quantity from entry field
    quantity = quantity_entered.get()
    if not quantity.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid quantity.")
        return

    # Send ADD request to server with product ID and quantity
    message = f"ADD,{product['id']},{quantity}"
    client.sendall(message.encode())

    # Receive and unpickle server response
    data = client.recv(BUF_SIZE)
    response = pickle.loads(data)
    messagebox.showinfo("Add to Cart", response)

    # Reset quantity field and hide quantity frame
    quantity_entered.delete(0, END)
    product['quantity_frame'].pack_forget()

    # Refresh product view and cart view (if open)
    view_products()
    if cart_frame.winfo_ismapped():
        view_cart()

def view_cart():
    """Display cart contents"""

    # Request cart data from server
    client.sendall("CART".encode())
    data = client.recv(BUF_SIZE)
    cart_data = pickle.loads(data)

    # Clear existing cart text display
    cart_text.delete(1.0, END)

    # If cart_data is empty, show message
    if isinstance(cart_data, str):
        cart_text.insert(END, cart_data)
    else:
        # Display each item in cart
        cart_text.insert(END, "Current content:")
        for item in cart_data["items"]:
            cart_text.insert(END, f"\nId: {item['id']}\nName: {item['name']}\n\
Quantity:{item['quantity']}\nPrice:${item['price']:.2f}\nTotal per item: ${item['total']:.2f}\n")

        # Display total cart amount
        cart_text.insert(END, f"\nTotal Amount in cart: ${cart_data['total_amount']:.2f}")

def remove_from_cart():
    """Remove item from cart using id and quantity entry"""
    # Get product ID and quantity from user entries
    product_id = product_id_entry.get()
    quantity = quantity_entry.get()

    # Validate input values
    if not product_id or not quantity.isdigit():
        messagebox.showerror("Input Error", "Please provide valid product ID and quantity.")
        return

    # Send REMOVE request to server
    message = f"REMOVE,{product_id},{quantity}"
    client.sendall(message.encode())

    # Receive and show server response
    data = client.recv(BUF_SIZE)
    response = pickle.loads(data)
    messagebox.showinfo("Remove from Cart", response)

    # Clear input fields
    product_id_entry.delete(0, END)
    quantity_entry.delete(0, END)

    # Refresh product and cart views
    view_products()
    if cart_frame.winfo_ismapped():
        view_cart()

def checkout():
    """Handle checkout and payment process"""
    # Send CHECKOUT request
    client.sendall("CHECKOUT".encode())
    confirmation = pickle.loads(client.recv(BUF_SIZE))

    # If cart is empty
    if isinstance(confirmation, str) and "empty" in confirmation.lower():
        messagebox.showinfo("Checkout", confirmation)
        return

    # Ask user to confirm checkout
    checkout_choice = messagebox.askyesno("Checkout", confirmation)
    if not checkout_choice:
        client.send(pickle.dumps("no"))
        result = pickle.loads(client.recv(BUF_SIZE))
        messagebox.showinfo("Checkout", result)
        return
    else:
        client.send(pickle.dumps("yes"))
        payment_msg = pickle.loads(client.recv(BUF_SIZE))

        # Create payment method selection window
        payment_window = Toplevel(root)
        payment_window.title("Payment method")
        payment_window.configure(bg="honeydew")

        # Center payment window
        payment_window_width = 250
        payment_window_height = 290
        root_width = root.winfo_screenwidth()
        root_height = root.winfo_screenheight()
        x = int((root_width / 2) - (payment_window_width / 2))
        y = int((root_height / 2) - (payment_window_height / 2))
        payment_window.geometry(f"{payment_window_width}x{payment_window_height}+{x}+{y}")

        # Set payment window icon
        payment_window.iconbitmap(r"pay_logo.ico")

        # Payment selection frame
        payment_frame = Frame(payment_window,
                              bg="white",
                              padx=10, pady=10)

        payment_frame.pack(padx=10, pady=10)

        # Payment message from server
        Label(payment_frame, text=payment_msg,
              bg="white",
              font=("Arial", 10),
              padx=5, pady=5).pack(padx=10, pady=10)

        # Payment options using radio buttons
        payment_method = StringVar()
        payment_method.set("1")

        Radiobutton(payment_frame,
                    text="Credit card",
                    font=("arial", 10),
                    variable=payment_method,
                    value=1).pack()

        Radiobutton(payment_frame,
                    text="Debit card",
                    font=("arial", 10),
                    variable=payment_method,
                    value=2).pack()

        Radiobutton(payment_frame,
                    text="Cash",
                    font=("arial", 10),
                    variable=payment_method,
                    value=3).pack()

        # Payment confirmation button
        def confirm_payment():
            choice = payment_method.get()
            client.send(pickle.dumps(choice))
            response = pickle.loads(client.recv(BUF_SIZE))
            messagebox.showinfo("Checkout", response)
            payment_window.destroy()

            # Reset cart text area after checkout
            cart_text.delete(1.0, END)
            cart_text.insert(END, "Your cart is empty")

        Button(payment_frame,
               text="Confirm Payment",
               bg="khaki",
               command=confirm_payment).pack(pady=5)

def show_analytics_chart():
    """Fetch transaction data and display pie chart analytics"""
    # Request analytics data from server
    client.sendall("ANALYTICS".encode())
    data = client.recv(BUF_SIZE)
    results = pickle.loads(data)

    # Clear existing widgets in analytics frame
    for widgets in analytics_frame.winfo_children():
        widgets.destroy()

    # If no transactions found
    if not results:
        Label(analytics_frame,
              text="No transactions found",
              font=("Arial", 10),
              bg="white").pack(padx=5, pady=5)
    else:
        # Extract product names and quantities sold
        labels = [row[0] for row in results]
        sizes = [row[1] for row in results]

        # Create matplotlib figure and pie chart
        fig, ax = plt.subplots(figsize=(3.2, 3.2))
        colours = ['salmon', 'royalblue', 'lavender', 'moccasin', 'orchid', 'turquoise']

        ax.pie(sizes,
               labels=labels,
               autopct='%1.1f%%',  # Percentages to 1 dp
               startangle=90,
               colors=colours)

        ax.axis('equal')  # Keep pie chart circular
        ax.set_title("Most Sold Products")

        # Embed matplotlib canvas into Tkinter analytics frame
        canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=5)


def show_sales_trends():
    try:
        # Request sales trend data from server
        client.sendall("PRODUCT_TRENDS".encode())
        response = pickle.loads(client.recv(BUF_SIZE))

        # Handle server response statuses
        if response.get("status") == "error":
            messagebox.showerror("Error", response["message"])
            return
        if response.get("status") == "empty":
            messagebox.showinfo("Info", response["message"])
            return

        data = response["data"]
        if not data:
            messagebox.showinfo("Info", "No data available for trends")
            return

        # Clear existing widgets in the sales trend frame
        for widget in sales_trend_frame.winfo_children():
            widget.destroy()

        # Matplotlib figure
        fig, ax = plt.subplots(figsize=(4,4))

        # Plot each product line
        colors = plt.cm.tab10.colors  # Predefined color palette
        for i, product in enumerate(data["products"]):
            ax.plot(
                data["user_ids"],   # X-axis: User IDs
                data["quantities"][i],   # Y-axis: Quantity purchased by each user
                color=colors[i % len(colors)],   # Cycle through colors
                linestyle='-',
                linewidth=0.7,
                label=product   # Add product name as label
            )

        # Set chart titles and labels
        ax.set_title("Product sales trend", pad=20)
        ax.set_xlabel("User", labelpad=10)
        ax.set_ylabel("Quantity Purchased", labelpad=10)

        # X-axis as integers for user IDs
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

        # Place legend inside the graph at upper right
        ax.legend(
            loc='upper right',  # Location
            framealpha=0.3,  # Transparent background
            edgecolor='black',  # Border color
            fontsize=5.2
        )

        # Add transparent grid behind graph
        ax.grid(True, alpha=0.1)

        plt.tight_layout()  # Automatically adjust axes, labels, etc spacing

        # Embed the Matplotlib chart into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=sales_trend_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)


    except Exception as e:
        messagebox.showerror("Error", f"Failed to display trends: {str(e)}")

def exit_client():
    """Safely send exit request to server, close connection and terminate application"""
    client.sendall("EXIT".encode())
    response = pickle.loads(client.recv(BUF_SIZE))
    messagebox.showinfo("Exit", response)
    client.close()
    print("Disconnected from server.")
    root.quit()

def build_top_bar():
    """Constructs the top navigation bar with buttons for cart, analytics, sales trends and exit"""
    # Cart button
    cart_button = Button(top_frame,
                         text="🛒",
                         font=("Arial", 13),
                         bg="yellow",
                         command=toggle_cart_frame)

    cart_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Analytics button
    analytics_button = Button(top_frame,
                              text="📊 Analytics",
                              font=("Arial", 9, "bold"),
                              bg="deepskyblue",
                              fg="white",
                              command=toggle_analytics_frame)

    analytics_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Sales trend button
    sales_trend_button = Button(
        top_frame,
        text="📊 Sales Trend",
        font=("Arial", 9, "bold"),
        bg="slateblue",
        fg="white",
        command=toggle_sales_trend_frame
    )
    sales_trend_button.grid(row=0, column=2, padx=5, pady=5)

    # Exit button
    exit_button = Button(top_frame,
                         text="❌ Exit",
                         bg="red",
                         fg="white",
                         font=("Arial", 9, "bold"),
                         command=exit_client)

    exit_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")


def build_welcome_content():
    # Contains the welcome message panel content
    welcome_text = """🌟 Welcome to Digital Shop! 🌟

Hi there! 👋 I'm your shopping helper.

To your left,

Browse our digital collection 🔍:
• 💽 Software & Licenses
• 📖 E-books & Guides
• 🎵 Music & Sound Packs

🛒 Your Shopping Cart:
• Real-time cart updates
• Secure checkout
• Different payment options

📊 See what's popular with Analytics

Happy shopping and don't leave 
without a purchase! 😊"""

    Label(welcome_frame,
          text=welcome_text,
          font=("Arial", 12),
          bg="white",
          justify=LEFT,
          wraplength=350
          ).pack(padx=5, pady=5)

def build_cart_content():
    global product_id_entry, quantity_entry, cart_text

    # Text display for cart contents
    cart_text_frame = Frame(cart_frame)
    cart_text_frame.pack(padx=5, pady=10)

    cart_text = Text(cart_text_frame,
                     width=41, height=16,
                     bg="white",
                     fg="black")

    cart_text.pack(side=LEFT, fill=Y)

    # Vertical scrollbar for cart text area
    cart_scrollbar = Scrollbar(cart_text_frame, command=cart_text.yview)
    cart_scrollbar.pack(side=RIGHT, fill=Y)
    cart_text.config(yscrollcommand=cart_scrollbar.set)

    # Product ID entry
    Label(cart_frame,
          text="Product ID: ",
          font=("Arial", 9, "bold")
          ).pack()

    product_id_entry = Entry(cart_frame)
    product_id_entry.pack()

    # Quantity entry
    Label(cart_frame,
          text="Quantity: ",
          font=("Arial", 9, "bold")
          ).pack()

    quantity_entry = Entry(cart_frame)
    quantity_entry.pack()

    # Remove item button
    Button(cart_frame,
           text="➖ Remove from Cart",
           font=("Arial", 9, "bold"),
           bg="orange",
           fg="white",
           command=remove_from_cart
           ).pack(pady=5)

    # Checkout button
    Button(cart_frame,
           text="Proceed to Checkout",
           bg="green",
           fg="white",
           font=("Arial", 9, "bold"),
           command=checkout
           ).pack(pady=5)

    # Close cart button
    Button(cart_frame,
           text="❌ Close Cart",
           bg="red",
           fg="white",
           font=("Arial", 9, "bold"),
           command=toggle_cart_frame
           ).pack(pady=5)

def main():
    build_top_bar()
    build_welcome_content()
    build_cart_content()
    show_login()
    root.mainloop()

if __name__ == "__main__":
    main()