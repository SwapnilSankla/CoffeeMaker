def my_decorator_function(func):

    def inner():
        print(f"Going to enter {func}")
        return func()
    return inner


@my_decorator_function
def hello_world():
    print("Hello world!!")


hello_world()
