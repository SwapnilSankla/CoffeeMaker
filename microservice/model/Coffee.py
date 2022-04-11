class Coffee:
    type = ""
    prerequisites = {}
    price = 0

    def __init__(self, type, prerequisites, price):
        self.type = type
        self.prerequisites = prerequisites
        self.price = price


class EspressoCoffee(Coffee):
    def __init__(self, prerequisites, price):
        Coffee.__init__(self, "espresso", prerequisites, price)


class LatteCoffee(Coffee):
    def __init__(self, prerequisites, price):
        Coffee.__init__(self, "latte", prerequisites, price)


class CappuccinoCoffee(Coffee):
    def __init__(self, prerequisites, price):
        Coffee.__init__(self, "cappuccino", prerequisites, price)