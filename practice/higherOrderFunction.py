def add(num1, num2):
    return num1 + num2


def calculate(num1, num2, fun):
    return fun(num1, num2)


print(calculate(10, 20, add))
