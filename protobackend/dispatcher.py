from functools import reduce, wrapper, partial
import json

def pipe(funcs, data):
    return reduce(lambda x, f: f(x), funcs, data)

class Dispatcher:
    def __init__(self, exercises):
        self.exercises = exercises
        self.active_exercise = None
        self._pre_hooks = []
        self._post_hooks = []
    
    def dispatch(data):

        if self.active_exercise is None:
            raise Exception("No active exercise")
        
        hook_output = pipe(pre_hooks, data)

        cmd = getattr(self.active_exercise, hook_output['command'])
        cmd_output = cmd(hook_output['payload'])

        return pipe(post_hooks, cmd_output)

    def hook(self, hook_type = 'pre'):
        def dec(f):
            pf = partial(f, self)
            if hook_type == 'pre': self._pre_hooks.append(pf)
            elif hook_type == 'post': self._post_hooks.append(pf)
            else: raise Exception("Invalid hook type: %s" %hook_type)

            return f
        return dec
