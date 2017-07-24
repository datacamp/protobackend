class BaseExercise:
    EXERCISE_TYPE = "Exercise"

    def runInit(self, data):
        raise Exception("Need to define a custom runInit method")

    def runSubmit(self, data):
        raise Exception("Need to define a custom runSubmit method")

    def runConsole(self, data):
        raise Exception("Need to define a custom runSubmit method")
