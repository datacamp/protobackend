from protobackend.dispatcher import Dispatcher
import pytest

class A:
    @staticmethod
    def do_stuff(data): return 'stuff'

    @staticmethod
    def get_x(data): return data.get('x', None)

class B:
    @staticmethod
    def get_y(data): return data.get('y', None)

@pytest.fixture
def d():
    d = Dispatcher(None)
    d.active_exercise = A
    return d


def test_simple(d):
    assert d.dispatch({'command': 'do_stuff', 'payload': {}}) == 'stuff'

def test_pre_hooks(d):
    @d.hook('pre')
    def add_1_to_x(payload, cmd):
        return {**payload, 'x': payload['x'] + 1}

    assert d.dispatch({'command': 'get_x', 'payload': {'x': 1}}) == 2

def test_post_hooks(d):
    @d.hook('post')
    def add_1_to_x(payload, cmd):
        return payload + 1

    assert d.dispatch({'command': 'get_x', 'payload': {'x': 1}}) == 2

def test_hook_dispatch_arg(d):
    @d.hook('pre')
    def set_active_ex(payload, cmd, dispatcher):
        dispatcher.active_exercise = B
        return payload

    assert d.dispatch({'command': 'get_y', 'payload': {'y': 2}}) == 2

def test_expose(d):
    get_x = d.expose('get_x')
    assert get_x({'x': 1}) == 1
