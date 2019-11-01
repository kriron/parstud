from parstud.reader.reader import build_database
from parstud.reader.reader import read_log
import sys
import os
import pytest
import pandas

# sys.path.append(os.path.abspath("../parstud/"))


def test_read_log():
    path = "tests/test_reader/input/out_test/output.0"

    funcs = read_log(path, 0)
    times = read_log(path, 1)

    assert isinstance(funcs, list) == True
    assert isinstance(times, list) == True

    assert isinstance(funcs[0], str) == True
    assert isinstance(times[0], float) == True

    with pytest.raises(TypeError):
        read_log(path, "123")
    with pytest.raises(ValueError):
        read_log(path, 123)
