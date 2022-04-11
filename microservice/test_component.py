import json

from server import create_test_server


def test_report():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        response = test_client.get('/coffee-maker/report')
        assert response.status_code == 200
        assert b'current resource values. e.g. \n water: 500ml \n milk: 500ml \n coffee: 100gm \n money: 0$' in response.data


def test_order_creation_insufficient_coins_scenario():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        request = {
            'coffeeType': 'espresso',
            'quarters': 3,
            'dimes': 0,
            'nickels': 0,
            'pennies': 0
        }
        response = test_client.post('/coffee-maker/order',
                                    data=json.dumps(request),
                                    content_type="application/json",
                                    )
        assert response.status_code == 422
        assert b"Sorry that's not enough money. Money refunded." in response.data


def test_order_creation_insufficient_resources_scenario():
    flask_app = create_test_server(10, 10, 0, 0)

    with flask_app.test_client() as test_client:
        request = {
            'coffeeType': 'espresso',
            'quarters': 30,
            'dimes': 0,
            'nickels': 0,
            'pennies': 0
        }
        response = test_client.post('/coffee-maker/order',
                                    data=json.dumps(request),
                                    content_type="application/json",
                                    )
        assert response.status_code == 500
        assert b"Sorry resources are not available!" in response.data


def test_order_creation_scenario():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        request = {
            'coffeeType': 'espresso',
            'quarters': 300,
            'dimes': 0,
            'nickels': 0,
            'pennies': 0
        }
        response = test_client.post('/coffee-maker/order',
                                    data=json.dumps(request),
                                    content_type="application/json",
                                    )
        assert response.status_code == 200


def test_order_get_not_found_scenario():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        response = test_client.get('/coffee-maker/orders/0')
        assert response.status_code == 404


def test_orders_get_found_scenario():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        request = {
            'coffeeType': 'espresso',
            'quarters': 300,
            'dimes': 0,
            'nickels': 0,
            'pennies': 0
        }
        response = test_client.post('/coffee-maker/order',
                                    data=json.dumps(request),
                                    content_type="application/json",
                                    )
        data = response.get_data()
        # TODO: Below line tells that response should be a json instead of string, fix it later
        order_id = str(data).split(':')[1].split('.')[0]
        response = test_client.get(f'/coffee-maker/orders/{order_id}')
        assert response.status_code == 200


def test_orders_get_all_scenario():
    flask_app = create_test_server(500, 500, 100, 0)

    with flask_app.test_client() as test_client:
        request = {
            'coffeeType': 'espresso',
            'quarters': 300,
            'dimes': 0,
            'nickels': 0,
            'pennies': 0
        }
        test_client.post('/coffee-maker/order',
                         data=json.dumps(request),
                         content_type="application/json",
                         )

        test_client.post('/coffee-maker/order',
                         data=json.dumps(request),
                         content_type="application/json",
                         )
        response = test_client.get('/coffee-maker/orders')
        json_data = json.loads(response.data)
        assert len(json_data) == 2
