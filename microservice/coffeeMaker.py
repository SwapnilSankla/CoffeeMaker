import random

from model.CurrencyConverter import CurrencyConverter
from model.Exception import NotSufficientResources, NotSufficientCoins
from model.Prerequisites import Prerequisites
from model.Coffee import EspressoCoffee, LatteCoffee, CappuccinoCoffee
from model.Order import Order


class CoffeeMaker:
    __water = 0
    __milk = 0
    __coffee = 0
    __money = 0
    __offerings = {}
    __orders = []

    def __init__(self, water=500, milk=500, coffee=100, money=0):
        self.__water = water
        self.__milk = milk
        self.__coffee = coffee
        self.__money = money
        self.__offerings = {
            "espresso": EspressoCoffee(Prerequisites(50, 0, 18), 1.00),
            "latte": LatteCoffee(Prerequisites(200, 150, 24), 2.00),
            "cappuccino": CappuccinoCoffee(Prerequisites(250, 100, 24), 4.00),
        }

    def __resource_available_for_making_coffee(self, coffee_type):
        if self.__water >= self.__offerings[coffee_type].prerequisites.water and \
                self.__milk >= self.__offerings[coffee_type].prerequisites.milk and \
                self.__coffee >= self.__offerings[coffee_type].prerequisites.coffeeBeans:
            return True
        else:
            return False

    def __inserted_coins_sufficient_to_make_coffee(self, coffee_type, inserted_coins_value):
        return inserted_coins_value > self.__offerings[coffee_type].price

    def test_setup(self, water, milk, coffee, money):
        self.__water = water
        self.__milk = milk
        self.__coffee = coffee
        self.__money = money
        self.__orders = []

    def get_orders(self):
        return self.__orders

    def report(self):
        return f"current resource values. e.g. \n water: {self.__water}ml \n milk: {self.__milk}ml \n coffee: {self.__coffee}gm \n money: {self.__money}$"

    def make(self, coffee_type, quarters, dimes, nickels, pennies):
        if not self.__resource_available_for_making_coffee(coffee_type):
            raise NotSufficientResources
        inserted_coins_value_in_dollars = CurrencyConverter.to_dollar(quarters, dimes, nickels, pennies)
        if not self.__inserted_coins_sufficient_to_make_coffee(coffee_type, inserted_coins_value_in_dollars):
            raise NotSufficientCoins

        order_id = random.randint(0, 10000)
        self.__water -= self.__offerings[coffee_type].prerequisites.water
        self.__milk -= self.__offerings[coffee_type].prerequisites.milk
        self.__coffee -= self.__offerings[coffee_type].prerequisites.coffeeBeans

        change = inserted_coins_value_in_dollars - self.__offerings[coffee_type].price
        self.__orders.append(Order(order_id, coffee_type, self.__offerings[coffee_type].price))
        return f"Order id: {order_id}. Here is your {coffee_type}. Enjoy!\nHere is ${round(change, 2)} in change."
