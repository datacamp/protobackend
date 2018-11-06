from os import path

class BaseExercise:
    EXERCISE_TYPE = "Exercise"

    def __init__(self, data, worker = None):
        self.dc_pec = data.get("DC_PEC", "")
        self.dc_sct = data.get("DC_SCT", "")
        self.dc_force_diagnose = data.get("DC_FORCE_DIAGNOSE", False)
        self.dc_sct_debug = data.get("DC_SCT_DEBUG", False)

        self.dc_solution = self._fmt_dc_code(data.get("DC_SOLUTION", ""))

        self.student_result = None
        self.solution_result = None

        # optional worker thread for queueing commands
        self.worker = worker

    def runInit(self, data):
        raise Exception("Need to define a custom runInit method")

    def runSubmit(self, data):
        raise Exception("Need to define a custom runSubmit method")

    def runConsole(self, data):
        raise Exception("Need to define a custom runSubmit method")

    @staticmethod
    def _fmt_dc_code(dc_code):
        if isinstance(dc_code, str):
            return dc_code

        get = lambda k: (entry.get(k) for entry in dc_code)
        paths = [path.join(*entry) for entry in zip(get('path'), get('name'))]
        return dict(zip(paths, get('content')))
