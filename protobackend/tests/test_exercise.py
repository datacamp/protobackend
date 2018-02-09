from protobackend.exercise import BaseExercise
import pytest

@pytest.fixture(scope = 'function')
def code_list():
    return [
            { 'name': 'script.sh', 'content': 'echo hey', 'path': '', 'isFolder': False },
            { 'name': '.bashrc', 'content': 'echo ya', 'path': 'a', 'isFolder': False }
            ]

def test_fmt_dc_code(code_list):
    out = BaseExercise._fmt_dc_code(code_list)

    assert out == { 'script.sh': 'echo hey', 'a/.bashrc': 'echo ya' }

def test_exercise_solution_list(code_list):
    ex = BaseExercise({ 'DC_SOLUTION': code_list })
    assert ex.dc_solution == {'script.sh': 'echo hey', 'a/.bashrc': 'echo ya'}

def test_exercise_solution_str(code_list):
    ex = BaseExercise({ 'DC_SOLUTION': "some code"})
    assert ex.dc_solution == "some code"

