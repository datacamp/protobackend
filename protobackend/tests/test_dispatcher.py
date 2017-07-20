from protobackend import Dispatcher

class A:
    @staticmethod
    def do_stuff(data): return 'stuff'

def test_simple():
    d = Dispatcher(None)
    d.active_exercise = A
    assert d.dispatch({'command': 'do_stuff', 'payload': None}) == 'stuff'
