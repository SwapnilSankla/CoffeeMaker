routes = {}


def process(path):
    return routes[path]()


def route(*non_key_word_args, **key_word_args):
    def inner(func):
        routes[key_word_args['path']] = func

    return inner


@route(path='/')
def get_all():
    print("get_all")


process('/')
