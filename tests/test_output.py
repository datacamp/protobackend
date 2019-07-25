from protobackend.output import safe_dump
import json
import pytest


def test_safe_dump():
    # Given
    @safe_dump
    def unsafe_func():
        raise Exception("uh-oh")

    # When
    result = json.dumps(unsafe_func())

    # Then
    assert (
        result
        == '"[{\\"type\\": \\"backend-error\\", \\"payload\\": \\"DataCamp encountered the following error:\\\\nuh-oh\\\\n\\"}]"'  # nopep8
        or result
        == '"[{\\"payload\\": \\"DataCamp encountered the following error:\\\\nuh-oh\\\\n\\", \\"type\\": \\"backend-error\\"}]"'  # nopep8
    )


def test_safe_dump_none():
    # Given
    @safe_dump
    def unsafe_func():
        return None

    # When
    result = json.dumps(unsafe_func())

    # Then
    assert result == '"[]"'


def test_safe_dump_invalid_type():
    # Given
    @safe_dump
    def unsafe_func():
        return {}

    # When
    with pytest.warns(Warning) as w:
        result = json.dumps(unsafe_func())

    # Then
    assert result == '"[]"'
    assert (
        w[0].message.args[0]
        == "Executed commands are expected to return a list or nothing"
    )
