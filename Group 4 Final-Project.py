import heapq

class Node:
    """Node for the linked list (used in purchase history)"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Linked list to maintain purchase history"""
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        if not self.head:
            print("No purchase history.")
            return
        current = self.head
        print("Purchase History:")
        while current:
            print(f"{current.data}")
            current = current.next

class Product:
    """Class to represent a single product"""
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.sales = 0

class TreeNode:
    """Node for the binary search tree"""
    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None

class ProductTree:
    """Binary search tree for managing products"""
    def __init__(self):
        self.root = None

    def insert(self, product):
        if self.root is None:
            self.root = TreeNode(product)
        else:
            self._insert_recursive(self.root, product)

    def _insert_recursive(self, node, product):
        if product.product_id < node.product.product_id:
            if node.left is None:
                node.left = TreeNode(product)
            else:
                self._insert_recursive(node.left, product)
        elif product.product_id > node.product.product_id:
            if node.right is None:
                node.right = TreeNode(product)
            else:
                self._insert_recursive(node.right, product)

    def search(self, product_id):
        return self._search_recursive(self.root, product_id)

    def _search_recursive(self, node, product_id):
        if node is None:
            return None
        if product_id == node.product.product_id:
            return node.product
        elif product_id < node.product.product_id:
            return self._search_recursive(node.left, product_id)
        else:
            return self._search_recursive(node.right, product_id)

    def in_order_traversal(self):
        products = []
        self._in_order_recursive(self.root, products)
        return products

    def _in_order_recursive(self, node, products):
        if node is not None:
            self._in_order_recursive(node.left, products)
            products.append(node.product)
            self._in_order_recursive(node.right, products)

class OnlineStore:
    def __init__(self):
        self.product_tree = ProductTree()  # Tree to store products
        self.top_selling = []  # Min-heap to track top-selling products (-sales used for max-heap behavior)
        self.purchase_history = LinkedList()  # Linked list to store purchase history

    # Add a new product
    def add_product(self, product_id, name, price, stock):
        existing_product = self.product_tree.search(product_id)
        if existing_product is not None:
            print(f"Product ID {product_id} already exists.")
            return
        new_product = Product(product_id, name, price, stock)
        self.product_tree.insert(new_product)
        print(f"Product '{name}' added successfully.")

    # Search products by ID
    def search_product_by_id(self, product_id):
        product = self.product_tree.search(product_id)
        if product is not None:
            print(f"Found: ID: {product.product_id}, Name: {product.name}, Price: ${product.price}, Stock: {product.stock}")
        else:
            print("Product not found.")

    # Purchase products and maintain top-selling list and purchase history
    def purchase(self, product_id, quantity):
        product = self.product_tree.search(product_id)
        if product is not None:
            if product.stock >= quantity:
                product.stock -= quantity
                product.sales += quantity
                total_cost = product.price * quantity
                heapq.heappush(self.top_selling, (-product.sales, product))
                self.purchase_history.add(f"Purchased {quantity} x {product.name} for ${total_cost:.2f}")
                print(f"Purchased {quantity} x {product.name}. Total: ${total_cost:.2f}")
            else:
                print(f"Insufficient stock for {product.name}. Available: {product.stock}")
        else:
            print("Product not found.")

    # Display top-selling products
    def display_top_selling(self, top_n=3):
        print(f"Top {top_n} best-selling products:")
        top_products = heapq.nsmallest(top_n, self.top_selling)
        for sales, product in top_products:
            print(f"{product.name} - Sold: {-sales}")

    # Display purchase history
    def display_purchase_history(self):
        self.purchase_history.display()

    # Display all products in the store
    def display_all_products(self):
        products = self.product_tree.in_order_traversal()
        if not products:
            print("No products available in the store.")
        else:
            print("All Products:")
            for product in products:
                print(f"ID: {product.product_id}, Name: {product.name}, Price: ${product.price}, Stock: {product.stock}")

# Interactive Usage
def main():
    store = OnlineStore()

    while True:
        print("\n1. Add Product")
        print("2. Search Product by ID")
        print("3. Purchase Product")
        print("4. Display Top-Selling Products")
        print("5. Display Purchase History")
        print("6. Display All Products")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            product_id = int(input("Enter Product ID: "))
            name = input("Enter Product Name: ")
            price = float(input("Enter Product Price: "))
            stock = int(input("Enter Product Stock: "))
            store.add_product(product_id, name, price, stock)
        elif choice == "2":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            product_id = int(input("Enter Product ID to Search: "))
            store.search_product_by_id(product_id)
        elif choice == "3":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            product_id = int(input("Enter Product ID to Purchase: "))
            quantity = int(input("Enter Quantity: "))
            store.purchase(product_id, quantity)
        elif choice == "4":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            top_n = int(input("Enter Number of Top-Selling Products to Display: "))
            store.display_top_selling(top_n)
        elif choice == "5":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            store.display_purchase_history()
        elif choice == "6":
            if input("Press 'b' to go back or any other key to continue: ") == 'b':
                continue
            store.display_all_products()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
