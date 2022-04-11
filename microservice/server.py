import json

from flask import Blueprint, Flask, Response, request
from coffeeMaker import CoffeeMaker
from model.Exception import NotSufficientResources, NotSufficientCoins

coffee_maker = Blueprint('coffee_maker', __name__)
coffeeMaker = CoffeeMaker()


@coffee_maker.route('/report')
def report():
    return coffeeMaker.report()


@coffee_maker.route('/orders')
def get_orders():
    return json.dumps(coffeeMaker.get_orders(),
                      default=lambda o: o.__dict__)


@coffee_maker.route('/orders/<order_id>')
def get_order(order_id):
    result = list(filter(lambda current_order: (current_order.orderId == int(order_id)), coffeeMaker.get_orders()))
    if len(result) == 0:
        return Response(status=404)
    return result[0].__dict__


@coffee_maker.route('/order', methods=["POST"])
def order():
    request_data = request.get_json()
    try:
        return (coffeeMaker.make(request_data["coffeeType"],
                                 request_data["quarters"],
                                 request_data["dimes"],
                                 request_data["nickels"],
                                 request_data["pennies"]))
    except NotSufficientResources:
        return Response(json.dumps({"error": "Sorry resources are not available!"}), status=500)
    except NotSufficientCoins:
        return Response(json.dumps({"error": "Sorry that's not enough money. Money refunded."}), status=422)


def create_server():
    app = Flask(__name__)
    app.register_blueprint(coffee_maker, url_prefix='/coffee-maker')
    return app


def create_test_server(water, milk, coffee, money):
    app = Flask(__name__)
    coffeeMaker.test_setup(water, milk, coffee, money)

    app.register_blueprint(coffee_maker, url_prefix='/coffee-maker')
    return app


server = create_server()
print("Supported endpoints:")
print("======================")
print(server.url_map)
print("======================")
print("\n")

if __name__ == "__main__":
    server.run()
