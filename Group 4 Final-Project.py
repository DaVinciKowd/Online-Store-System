class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0  # Counter to track the number of nodes

    def add(self, data):
        """Add a new node at the beginning of the linked list"""
        new_node = LinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1  # Increment size when adding a new node

    def display(self):
        """Display all nodes in the linked list"""
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def generate_id(self):
        """Generate a new unique ID based on the current size"""
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
        # Search for a product by name (case-sensitive)
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

class OnlineStore:
    def __init__(self):
        self.product_tree = ProductTree()  # Tree to store products
        self.top_selling = MaxHeap()  # Max-heap to track top-selling products
        self.purchase_history = LinkedList()  # Linked list to store purchase history
        self.product_list = LinkedList()  # Linked list to track added products

    def add_product(self, name, price, stock):
        """Automatically generate a product ID and add a new product"""
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
        # Search for a product by name (case-sensitive)
        product = self.product_tree.search_by_name(name)
        if product is not None:
            print(f"Found: ID: {product.product_id}, Name: {product.name}, Price: ₱{product.price}, Stock: {product.stock}")
        return product

    def purchase(self, product_identifier, quantity):
        # Try to search by ID first
        if product_identifier.isdigit():
            product_id = int(product_identifier)
            product = self.search_product_by_id(product_id)
        else:
            # If it's not an ID, assume it's a name
            product = self.search_product_by_name(product_identifier)

        if product is not None:
            # Display product details before asking for quantity
            print(f"Product Details: Name: {product.name}, Price: ₱{product.price}, Stock: {product.stock}")
            if product.stock >= quantity:
                product.stock -= quantity
                product.sales += quantity
                total_cost = product.price * quantity
                self.top_selling.push((product.sales, product))
                self.purchase_history.add(f"Purchased {quantity} x {product.name} for ₱{total_cost:.2f}")
                print(f"Purchased {quantity} x {product.name}. Total: ₱{total_cost:.2f}")
            else:
                print(f"Insufficient stock for {product.name}. Available: {product.stock}")
        else:
            print("Product not found.")

    def display_top_selling(self, top_n=3):
        print(f"Top {top_n} best-selling products:")
        top_products = []
        for _ in range(top_n):
            top_product = self.top_selling.pop()
            if top_product:
                sales, product = top_product
                top_products.append(f"{product.name} - Sold: {sales}")
        
        for product in top_products:
            print(product)

    def display_purchase_history(self):
        self.purchase_history.display()

    def display_all_products(self):
        products = self.product_tree.in_order_traversal()
        if not products:
            print("No products available in the store.")
        else:
            print("All Products:")
            for product in products:
                print(f"ID: {product.product_id}, Name: {product.name}, Price: ₱{product.price}, Stock: {product.stock}")

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
            name = input("Enter Product Name: ")
            price = float(input("Enter Product Price: "))
            stock = int(input("Enter Product Stock: "))
            store.add_product(name, price, stock)
        elif choice == "2":
            product_id = int(input("Enter Product ID to Search: "))
            store.search_product_by_id(product_id)
        elif choice == "3":
            product_identifier = input("Enter Product Name or ID to Purchase: ")
            quantity = int(input("Enter Quantity: "))
            store.purchase(product_identifier, quantity)
        elif choice == "4":
            top_n = int(input("Enter Number of Top-Selling Products to Display: "))
            store.display_top_selling(top_n)
        elif choice == "5":
            store.display_purchase_history()
        elif choice == "6":
            store.display_all_products()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
