from functools import reduce, wraps, partial
import inspect
import json
import pdb

def pipe(funcs, data, **kwargs):
    return reduce(lambda x, f: f(x, **kwargs), funcs, data)

class Dispatcher:
    def __init__(self, exercises, error_handler=None):
        self.exercises = exercises
        self.active_exercise = None
        self._pre_hooks = []
        self._post_hooks = []
        # TODO: error handling
        self.error_handler = error_handler
    
    def dispatch(self, data):
        cmd_name = data['command']
        pre_payload = pipe(self._pre_hooks, data['payload'], cmd = cmd_name)

        if self.active_exercise is None:
            raise Exception("No active exercise")

        cmd = getattr(self.active_exercise, cmd_name)
        cmd_output = cmd(pre_payload)

        post_payload = pipe(self._post_hooks, cmd_output, cmd = cmd_name)

        return post_payload

    def hook(self, hook_type):
        def dec(f):
            dispatch_arg = 'dispatcher' in inspect.signature(f).parameters
            pf = partial(f, dispatcher = self) if dispatch_arg else f

            if   hook_type == 'pre':  self._pre_hooks.append(pf)
            elif hook_type == 'post': self._post_hooks.append(pf)
            else: raise Exception("Invalid hook type: %s" %hook_type)

            return f
        return dec

    def expose(self, cmd_name):
        def f(payload):
            return self.dispatch({'command': cmd_name, 'payload': payload})

        return f

    def _expose_run(self, cmd_name):
        """For backwards compatibility.
        
        Commands.py used a function like console, to call a method named runConsole.
        """
        def f(payload):
            return self.dispatch({'command': 'run' + cmd_name.title(), 'payload': payload})

        return f
