class Order:
    orderId = 0
    coffeeType = ""
    price = 0.0

    def __init__(self, order_id, coffee_type, price):
        self.orderId = order_id
        self.coffeeType = coffee_type
        self.price = price
