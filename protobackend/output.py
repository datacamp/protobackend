import os
import traceback as Traceback
import json
import functools

class CaptureErrors(object):

    TYPE = "type"
    TYPE_VALUE = "backend-error"
    capture = True

    def __init__(self, output):
        self.output = output
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exception, traceback):
        if exc_type is None:
            return

        debug = os.environ.get('SQL_BACKEND_DEBUG') or os.environ.get('DC_BACKEND_DEBUG')
        if debug == "True" :
            error_message = Traceback.format_exception(exc_type, exception, traceback)
        elif debug == "raise":
            raise exception
        else :
            error_message = str(exception)

        entire_message = "DataCamp encountered the following error:\n{0}\n".format(error_message)
        self.output.append({"type": "backend-error", "payload": entire_message})
        return CaptureErrors.capture

    @classmethod
    def isCaptureErrorOutput(cls, output):
        if isinstance(output, list):
            for d in output:
                if isinstance(d,dict):
                    for k,v in d.items():
                        if k == cls.TYPE and v == cls.TYPE_VALUE:
                            return True
        return False


def safe_dump(f, json_dumper=None):
    """Wrapper which dumps output to json. In case of error, dump error to json."""

    json_dumper = json.dumps if json_dumper is None else json_dumper

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        fallback_output = []
        with CaptureErrors(fallback_output):
            output = f(*args, **kwargs)
            return json_dumper(output)

        return json_dumper(fallback_output)
    return wrapper

def print_output(s):
    print("\n[1] %s\n\n>>> " % json.dumps(s))

def output_dec(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        s = f(*args, **kwargs)
        print_output(s)
        return s
    return wrapper
