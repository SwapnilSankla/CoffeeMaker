from unittest import TestCase

from coffeeMaker import CoffeeMaker
from model.Exception import NotSufficientResources, NotSufficientCoins


class TestCoffeeMaker(TestCase):
    def test_report(self):
        coffeemaker = CoffeeMaker(300, 200, 50, 10)
        expected_report = "current resource values. e.g. \n water: 300ml \n milk: 200ml \n coffee: 50gm \n money: 10$"
        actual_report = coffeemaker.report()
        self.assertEqual(expected_report, actual_report, "Expected report string does not match the actual one")

    def test_make_raises_resource_not_sufficient_if_resources_are_insufficient(self):
        coffeemaker = CoffeeMaker(water=10, milk=200, coffee=50, money=10)
        self.assertRaises(NotSufficientResources, coffeemaker.make, "espresso", 100, 0, 0, 0)

    def test_make_raises_coins_not_sufficient_if_coins_are_insufficient(self):
        coffeemaker = CoffeeMaker(water=100, milk=200, coffee=50, money=0)
        self.assertRaises(NotSufficientCoins, coffeemaker.make, "espresso", 0, 0, 0, 0)

    def test_make_returns_change_if_extra_coins_are_inserted(self):
        coffeemaker = CoffeeMaker(water=100, milk=200, coffee=50, money=0)
        result = coffeemaker.make("espresso", 10, 10, 10, 10)
        self.assertNotEqual(result.find("Here is $3.1 in change."), -1)

    def test_make_reduces_resources_according_to_the_order(self):
        coffeemaker = CoffeeMaker(water=100, milk=200, coffee=50, money=0)
        expected_report = "current resource values. e.g. \n water: 50ml \n milk: 200ml \n coffee: 32gm \n money: 0$"
        coffeemaker.make("espresso", 10, 0, 0, 0)
        actual_report = coffeemaker.report()
        self.assertEqual(expected_report, actual_report)
