class BaseExercise:
    EXERCISE_TYPE = "Exercise"

    def __init__(self, data, worker = None):
        self.dc_pec = data.get("DC_PEC", "")
        self.dc_solution = data.get("DC_SOLUTION", "")
        self.dc_sct = data.get("DC_SCT", "")
        self.dc_sct_debug = data.get("DC_SCT_DEBUG", False)

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
