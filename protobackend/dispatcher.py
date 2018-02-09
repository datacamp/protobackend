from functools import reduce, wraps, partial
import inspect
import json
import os

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
        """Decorator for creating pre/post dispatch hooks.
        
        Arguments:
            hook_type: either "pre" or "post", depending on hook.
        """

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

    def _expose_run(self, cmd_name, dispatch = None):
        """For backwards compatibility.
        
        Commands.py used a function like console, to call a method named runConsole.
        """

        dispatch = self.dispatch if dispatch is None else dispatch

        def f(payload):
            # convert to camel case
            cml_cmd = "run" + "".join([wrd.title() for wrd in cmd_name.split('_')])

            return dispatch({'command': cml_cmd, 'payload': payload})

        return f

# Misc hooks ------------------------------------------------------------------

def init_hook(data, cmd, dispatcher):
    if cmd == 'runInit':
        dc_type = data.get('DC_TYPE')

        # choose exercise, based on dc_type
        try: ExCls = dispatcher.exercises[dc_type]
        except KeyError:
            error_msg = "Exercise type {} not one of {}".format(
                            dc_type,
                            ", ".join(dispatcher.exercises.keys())
                            )
            raise KeyError(error_msg)

        dispatcher.active_exercise = ExCls(data)
    
    return data


def fs_hook(data, cmd, dispatcher):
    dc_code = data.get("DC_CODE")
    if isinstance(dc_code, list):
        for entry in dc_code: fs_save(**entry)

    return data


def fs_save(name, content, isFolder, path, **kwargs):
    """Save a file or folder to disk.  Makes intermediate directories."""

    full_path = os.path.join(path, name)

    dirname = full_path if isFolder else os.path.dirname(full_path)
    mkdir_p(dirname)

    if not isFolder:
        with open(full_path, 'w') as f: f.write(content)

def mkdir_p(path):
    try: os.makedirs(path)
    except FileExistsError: pass



# Worker thread ---------------------------------------------------------------

import threading
from queue import Queue, Empty
class WorkerThread(threading.Thread):
    def __init__(self, dispatch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q_command = Queue()
        self.q_result = Queue()
        self.stop_request = threading.Event()
        self.dispatch = dispatch

    def run(self):
        while not self.stop_request.is_set():
            try:
                cmd = self.q_command.get(True, 0.05)
                self.q_result.put((cmd, self.dispatch(cmd)))
                self.q_command.task_done()
            except Empty:
                continue

    def join(self, timeout = None):
        self.stop_request.set()
        super().join(timeout)

