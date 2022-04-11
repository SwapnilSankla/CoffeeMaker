class CurrencyConverter:
    @staticmethod
    def to_dollar(quarters, dimes, nickles, pennies):
        dollar = 0.0
        dollar += quarters / 4
        dollar += dimes / 10
        dollar += nickles / 20
        dollar += pennies / 100
        return round(dollar, 2)