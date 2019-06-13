from protobackend.dispatcher import Dispatcher, fs_hook, fs_save
import tempfile
import os
import pytest
from pathlib import Path


class A:
    @staticmethod
    def do_stuff(data):
        return "stuff"

    @staticmethod
    def get_x(data):
        return data.get("x", None)


class B:
    @staticmethod
    def get_y(data):
        return data.get("y", None)


@pytest.fixture
def d():
    d = Dispatcher(None)
    d.active_exercise = A
    return d


def test_simple(d):
    assert d.dispatch({"command": "do_stuff", "payload": {}}) == "stuff"


def test_pre_hooks(d):
    @d.hook("pre")
    def add_1_to_x(payload, cmd):
        return {**payload, "x": payload["x"] + 1}

    assert d.dispatch({"command": "get_x", "payload": {"x": 1}}) == 2


def test_post_hooks(d):
    @d.hook("post")
    def add_1_to_x(payload, cmd):
        return payload + 1

    assert d.dispatch({"command": "get_x", "payload": {"x": 1}}) == 2


def test_hook_dispatch_arg(d):
    @d.hook("pre")
    def set_active_ex(payload, cmd, dispatcher):
        dispatcher.active_exercise = B
        return payload

    assert d.dispatch({"command": "get_y", "payload": {"y": 2}}) == 2


def test_fs_hook_file(d):
    d.hook("pre")(fs_hook)
    with tempfile.TemporaryDirectory() as td:
        dc_code = [
            {
                "name": "script.py",
                "content": "print(1 + 1)",
                "isFolder": False,
                "path": td,
            }
        ]

        d.dispatch({"command": "do_stuff", "payload": {"DC_CODE": dc_code}})

        fname = os.path.join(td, "script.py")
        assert os.path.isfile(fname)
        assert open(fname).read() == dc_code[0]["content"]


def test_fs_hook_folder(d):
    d.hook("pre")(fs_hook)
    with tempfile.TemporaryDirectory() as td:
        dc_code = [{"name": "some_folder", "content": "", "isFolder": True, "path": td}]

        d.dispatch({"command": "do_stuff", "payload": {"DC_CODE": dc_code}})
        assert os.path.isdir(os.path.join(td, "some_folder"))


def test_fs_save_makes_dirs():
    with tempfile.TemporaryDirectory() as td:
        fs_save("a/b/c.txt", "yo", isFolder=False, path=td)

        assert (Path(td) / "a/b").is_dir()
        assert (Path(td) / "a/b/c.txt").is_file()


def test_expose(d):
    get_x = d.expose("get_x")
    assert get_x({"x": 1}) == 1
