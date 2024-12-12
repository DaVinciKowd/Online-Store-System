import tkinter as tk
from tkinter import messagebox

class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0  # Counter to track the number of nodes

    def add(self, data):
        new_node = LinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1  # Increment size when adding a new node

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def generate_id(self):
        #Generate a new unique ID based on the current size
        return self.size + 1  # Use size+1 for a simple unique ID

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.sales = 0  # Track the number of units sold

class ProductTree:
    def __init__(self):
        self.products = {}

    def insert(self, product):
        self.products[product.product_id] = product

    def search(self, product_id):
        return self.products.get(product_id, None)

    def search_by_name(self, name):
        """Search for a product by name (case-sensitive)"""
        for product in self.products.values():
            if product.name.lower() == name.lower():
                return product
        return None

    def in_order_traversal(self):
        return sorted(self.products.values(), key=lambda x: x.product_id)

class MaxHeap:
    """Simple Max-Heap implementation"""
    def __init__(self):
        self.heap = []

    def push(self, item):
        """Push item to the heap and maintain the heap property"""
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """Pop the largest item from the heap"""
        if len(self.heap) == 0:
            return None
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._heapify_down(0)
        return item

    def _heapify_up(self, index):
        """Move the item at index up to maintain the heap property"""
        parent = (index - 1) // 2
        if index > 0 and self.heap[parent][0] < self.heap[index][0]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        """Move the item at index down to maintain the heap property"""
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left
        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i, j):
        """Swap elements at indices i and j"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def peek(self):
        """Return the largest element without removing it"""
        if len(self.heap) > 0:
            return self.heap[0]
        return None

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def display(self):
        if not self.items:
            print("Your cart is empty.")
        else:
            for item in self.items:
                print(f"{item.product.name} (ID: {item.product.product_id}) - {item.quantity} x ₱{item.product.price}")

    def clear(self):
        self.items = []

    def view_cart(self):
        if not self.items:
            return "Your cart is empty."
        message = "Your Cart:\n"
        for item in self.items:
            message += f"{item.product.name} (ID: {item.product.product_id}) - {item.quantity} x ₱{item.product.price}\n"
        return message

# Decorator function to ensure consistent window size
def consistent_window_size(func):
    def wrapper(self, *args, **kwargs):
        new_win = func(self, *args, **kwargs)  # Call the original function
        if new_win:
            new_win.geometry("400x300")  # Set the size of the new window
        return new_win
    return wrapper

class OnlineStore:
    def __init__(self):
        self.product_tree = ProductTree()  # Tree to store products
        self.top_selling = MaxHeap()  # Max-heap to track top-selling products
        self.purchase_history = LinkedList()  # Linked list to store purchase history
        self.product_list = LinkedList()  # Linked list to track added products
        self.cart = Cart()  # Initialize the cart

    def add_sample_products(self):
        sample_products = [
            Product(1, "Laptop", 45000.00, 10),     # Product ID: 1, Price: 45,000 PHP, Stock: 10
            Product(2, "Smartphone", 20000.00, 25), # Product ID: 2, Price: 20,000 PHP, Stock: 25
            Product(3, "Headphones", 1500.00, 50),  # Product ID: 3, Price: 1,500 PHP, Stock: 50
            Product(4, "Monitor", 8000.00, 15),     # Product ID: 4, Price: 8,000 PHP, Stock: 15
            Product(5, "Keyboard", 1000.00, 100),   # Product ID: 5, Price: 1,000 PHP, Stock: 100
        ]
        for product in sample_products:
            self.product_tree.insert(product)

    def add_product(self, name, price, stock):
        product_id = self.product_list.generate_id()  # Generate unique ID
        new_product = Product(product_id, name, price, stock)
        self.product_tree.insert(new_product)
        self.product_list.add(new_product)  # Add product to the linked list
        print(f"Product '{name}' with ID {product_id} added successfully.")

    def search_product_by_id(self, product_id):
        product = self.product_tree.search(product_id)
        if product is not None:
            print(f"Found: ID: {product.product_id}, Name: {product.name}, Price: ₱{product.price}, Stock: {product.stock}")
        return product

    def search_product_by_name(self, name):
        product = self.product_tree.search_by_name(name)
        if product is not None:
            print(f"Found: ID: {product.product_id}, Name: {product.name}, Price: ₱{product.price}, Stock: {product.stock}")
        return product

    def add_to_cart(self, product_identifier, quantity):
        # Try to search by ID first
        if product_identifier.isdigit():
            product_id = int(product_identifier)
            product = self.search_product_by_id(product_id)
        else:
            # If it's not an ID, assume it's a name
            product = self.search_product_by_name(product_identifier)

        if product is not None:
            if product.stock >= quantity:
                self.cart.add_item(product, quantity)
                print(f"{quantity} x {product.name} added to your cart.")
            else:
                print(f"Insufficient stock for {product.name}. Available: {product.stock}")
        else:
            print("Product not found.")

    def purchase_cart(self):
        if not self.cart.items:
            print("Your cart is empty.")
            return

        total_cost = 0
        for item in self.cart.items:
            product = item.product
            quantity = item.quantity
            total_cost += product.price * quantity
            product.stock -= quantity
            product.sales += quantity
            self.top_selling.push((product.sales, product))
            self.purchase_history.add(f"Purchased {quantity} x {product.name} for ₱{product.price * quantity:.2f}")

        print(f"Total Purchase: ₱{total_cost:.2f}")
        self.cart.clear()  # Clear the cart after purchase

    def display_top_selling(self, top_n=3):
        print(f"Top {top_n} best-selling products:")
        top_products = self.top_selling.heap
        if not top_products:
            message = "No top-selling products found."
        else:
            message = f"Top {len(top_products)} best-selling products:\n"
            for sales, product in top_products[:3]:  # Show top 3 best-selling products
                message += f"{product.name} - Sold: {sales}\n"
        return message

    def display_purchase_history(self):
        purchase_history = self.purchase_history
        message = "Purchase History:\n" if purchase_history else "No purchase history available."
        current = purchase_history.head
        while current:
            message += current.data + "\n"
            current = current.next
        return message

    def display_all_products(self):
        products = self.product_tree.in_order_traversal()
        message = "All Products:\n" if products else "No products available in the store."
        for product in products:
            message += f"ID: {product.product_id} | Name: {product.name} | Price: ₱{product.price} | Stock: {product.stock}\n"
        return message

class OnlineStoreUI:
    def __init__(self, root, store):
        self.root = root
        self.store = store

        # UI setup
        self.root.title("DAVIRA")
        self.root.geometry("600x500")

        title_label = tk.Label(self.root, text="Welcome to DAVIRA Store", font=("Helvetica", 16))
        title_label.pack(pady=20)
        
        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product_ui, width=20)
        self.add_product_button.pack(pady=10)

        self.search_product_button = tk.Button(self.root, text="Search Product", command=self.search_product_ui, width=20)
        self.search_product_button.pack(pady=10)

        self.add_to_cart_button = tk.Button(self.root, text="Add to Cart", command=self.add_to_cart_ui, width=20)
        self.add_to_cart_button.pack(pady=10)

        self.view_cart_button = tk.Button(self.root, text="View Cart", command=self.view_cart_ui, width=20)
        self.view_cart_button.pack(pady=10)

        self.checkout_button = tk.Button(self.root, text="Checkout", command=self.checkout_ui, width=20)
        self.checkout_button.pack(pady=10)

        self.top_selling_button = tk.Button(self.root, text="Top Selling Products", command=self.view_top_selling_ui, width=20)
        self.top_selling_button.pack(pady=10)

        self.display_all_button = tk.Button(self.root, text="Display All Products", command=self.display_all_products_ui, width=20)
        self.display_all_button.pack(pady=10)

    @consistent_window_size
    def add_product_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Add Product")

        name_label = tk.Label(new_win, text="Product Name")
        name_label.pack(pady=5)
        name_entry = tk.Entry(new_win)
        name_entry.pack(pady=5)

        price_label = tk.Label(new_win, text="Price")
        price_label.pack(pady=5)
        price_entry = tk.Entry(new_win)
        price_entry.pack(pady=5)

        stock_label = tk.Label(new_win, text="Stock")
        stock_label.pack(pady=5)
        stock_entry = tk.Entry(new_win)
        stock_entry.pack(pady=5)

        def submit():
            name = name_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())
            self.store.add_product(name, price, stock)
            new_win.destroy()

        submit_button = tk.Button(new_win, text="Add Product", command=submit)
        submit_button.pack(pady=10)

        return new_win

    @consistent_window_size
    def search_product_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Search Product")

        search_label = tk.Label(new_win, text="Enter Product Name or ID")
        search_label.pack(pady=5)
        search_entry = tk.Entry(new_win)
        search_entry.pack(pady=5)

        def submit():
            product_identifier = search_entry.get()
            if product_identifier.isdigit():
                self.store.search_product_by_id(int(product_identifier))
            else:
                self.store.search_product_by_name(product_identifier)
            new_win.destroy()

        submit_button = tk.Button(new_win, text="Search Product", command=submit)
        submit_button.pack(pady=10)

        return new_win

    @consistent_window_size
    def add_to_cart_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Add to Cart")

        product_label = tk.Label(new_win, text="Enter Product Name or ID")
        product_label.pack(pady=5)
        product_entry = tk.Entry(new_win)
        product_entry.pack(pady=5)

        quantity_label = tk.Label(new_win, text="Enter Quantity")
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(new_win)
        quantity_entry.pack(pady=5)

        def submit():
            product_identifier = product_entry.get()
            quantity = int(quantity_entry.get())
            self.store.add_to_cart(product_identifier, quantity)
            new_win.destroy()

        submit_button = tk.Button(new_win, text="Add to Cart", command=submit)
        submit_button.pack(pady=10)

        return new_win

    @consistent_window_size
    def view_cart_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("View Cart")

        message = self.store.cart.view_cart()

        cart_label = tk.Label(new_win, text=message, justify=tk.LEFT)
        cart_label.pack(pady=10)

        return new_win


    @consistent_window_size
    def checkout_ui(self):
        # Show confirmation dialog
        confirmation = messagebox.askyesno(
            "Confirm Purchase",  # Title of the dialog
            "Are you sure you want to proceed with the checkout?"  # Message in the dialog
        )
        
        if confirmation:  # If the user clicked "Yes"
            self.store.purchase_cart()  # Process the cart purchase
            new_win = tk.Toplevel(self.root)
            new_win.title("Checkout")

            # Thank you message after the purchase
            message = "Thank you for your purchase!"
            checkout_label = tk.Label(new_win, text=message, font=("Helvetica", 14))
            checkout_label.pack(pady=10)

        else:  # If the user clicked "No"
            messagebox.showinfo("Purchase Canceled", "Your purchase has been canceled.")

        return new_win

    @consistent_window_size
    def view_top_selling_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Top Selling Products")

        message = self.store.display_top_selling()

        top_selling_label = tk.Label(new_win, text=message, justify=tk.LEFT)
        top_selling_label.pack(pady=10)

        return new_win

    @consistent_window_size
    def display_all_products_ui(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("All Products")

        message = self.store.display_all_products()

        all_products_label = tk.Label(new_win, text=message, justify=tk.LEFT)
        all_products_label.pack(pady=10)

        return new_win


if __name__ == "__main__":
    store = OnlineStore()
    store.add_sample_products() 
    root = tk.Tk()
    ui = OnlineStoreUI(root, store)
    root.mainloop()
