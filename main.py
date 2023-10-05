from abc import ABC, abstractmethod

# Base Product Class with Abstract Method for Cloning
class Product(ABC):
    def __init__(self, name, price, available=True):
        self.name = name
        self.price = price
        self.available = available

    @abstractmethod
    def clone(self):
        #  Method to create and return a copy of the product
        pass

# Laptop product class inheriting from Product
class Laptop(Product):
    def __init__(self, available=True):
        super().__init__("Laptop", 1000, available)

    def clone(self):
        # Return a new instance of the Laptop
        return Laptop()

# Headphones product class inheriting from Product
class Headphones(Product):
    def __init__(self, available=True):
        super().__init__("Headphones", 50, available)

    def clone(self):
        # Return a new instance of the Headphones
        return Headphones()

# Mobile product class inheriting from Product    
class Mobile(Product):
    def __init__(self, available=True):
        super().__init__("Mobile", 350, available)

    def clone(self):
        # Return a new instance of the Mobile
        return Mobile()

# Base Discount Strategy class with Abstract Method for Applying Discount
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price, quantity):
        # Method to compute and return the discounted price
        pass

# No Discount Strategy class 
class NoDiscount(DiscountStrategy):
    def apply_discount(self, price, quantity):
        # Return the original price (no discount applied)
        return price * quantity

# Percentage-based Discount Strategy class
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, price, quantity):
        # Apply the percentage discount and return the new price
        discounted_price = price * (1 - self.percentage / 100)
        return discounted_price * quantity

# Cart Item class to represent individual items in the shopping cart
class CartItem:
    def __init__(self, product, quantity, discount_strategy):
        self.product = product
        self.quantity = quantity
        self.discount_strategy = discount_strategy

    def calculate_total_price(self):
        # Calculate and return the total price of this cart item after applying discounts
        return self.discount_strategy.apply_discount(self.product.price, self.quantity)


# Shopping Cart class to hold cart items and manage them
class ShoppingCart:
    def __init__(self):
        self.cart_items = []

    def add_item(self, product, quantity, discount_strategy):
        # Add a product to the cart with the specified quantity and discount strategy
        cloned_product = product.clone()
        cart_item = CartItem(cloned_product, quantity, discount_strategy)
        self.cart_items.append(cart_item)

    def update_quantity(self, product_name, new_quantity):
        # Update the quantity of the specified product in the cart
        for item in self.cart_items:
            if item.product.name == product_name:
                item.quantity = new_quantity
                return True
        return False

    def remove_item(self, product_name):
        # Remove the specified product from the cart
        self.cart_items = [
            item for item in self.cart_items if item.product.name != product_name]

    def calculate_total_bill(self):
        # Calculate and return the total bill for the items in the cart
        total_bill = 0
        for item in self.cart_items:
            total_bill += item.calculate_total_price()
        return total_bill

# Example usage: Command-line interface for the shopping cart
if __name__ == "__main__":
    cart = ShoppingCart()

# Command-line loop to interact with the shopping cart
    while True:
        print("\nAvailable Products: Laptop, Headphones, Mobile")
        action = input("Enter 'add', 'update', 'remove', or 'done': ").lower()

        if action == 'done':
            break

        if action == 'add':
            product_name = input("Enter product name: ").capitalize()
            quantity = int(input("Enter quantity: "))
            discount = float(
                input("Enter discount percentage (0 for no discount): "))

            if product_name == 'Laptop':
                product = Laptop()
            elif product_name == 'Headphones':
                product = Headphones()
            elif product_name == 'Mobile':
                product = Mobile()
            else:
                print("Invalid product name.")
                continue

            if discount == 0:
                discount_strategy = NoDiscount()
            else:
                discount_strategy = PercentageDiscount(discount)

            cart.add_item(product, quantity, discount_strategy)

        elif action == 'update':
            product_name = input(
                "Enter product name to update quantity: ").capitalize()
            new_quantity = int(input("Enter new quantity: "))
            cart.update_quantity(product_name, new_quantity)

        elif action == 'remove':
            product_name = input("Enter product name to remove: ").capitalize()
            cart.remove_item(product_name)

        else:
            print("Invalid action. Please try again.")

 # Display the cart items and total bill
    print("\nCart Items:")
for item in cart.cart_items:
    discounted_price_per_item = item.discount_strategy.apply_discount(
        item.product.price, 1)
    item_price = item.calculate_total_price()
    print(f"{item.quantity} {item.product.name} @ ${discounted_price_per_item} each (Original: ${item.product.price}) = ${item_price}")
print("Total Bill: ${}".format(cart.calculate_total_bill()))
