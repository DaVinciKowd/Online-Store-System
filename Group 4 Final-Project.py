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
                self.top_selling.push((product.sales, product))
                self.purchase_history.add(f"Purchased {quantity} x {product.name} for ${total_cost:.2f}")
                print(f"Purchased {quantity} x {product.name}. Total: ${total_cost:.2f}")
            else:
                print(f"Insufficient stock for {product.name}. Available: {product.stock}")
        else:
            print("Product not found.")

    # Display top-selling products
    def display_top_selling(self, top_n=3):
        print(f"Top {top_n} best-selling products:")
        top_products = []
        for _ in range(top_n):
            top_product = self.top_selling.pop()
            if top_product:
                sales, product = top_product
                top_products.append(f"{product.name} - Sold: {sales}")
        
        # Re-insert the products back into the heap if needed
        for product in top_products:
            self.top_selling.push(product)
        
        for product in top_products:
            print(product)

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
