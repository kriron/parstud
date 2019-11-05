from parstud.reader.reader import build_database
from parstud.reader.reader import read_log
import sys
import os
import pytest
import pandas as pd


def test_read_log():
    path = "tests/test_reader/input/out_test/output.0"

    funcs = read_log(path, 0)
    times = read_log(path, 1)

    assert isinstance(funcs, list)
    assert isinstance(times, list)

    assert isinstance(funcs[0], str)
    assert isinstance(times[0], float)

    assert len(times) == 7
    assert len(funcs) == len(times)

    with pytest.raises(TypeError):
        read_log(path, "123")
    with pytest.raises(ValueError):
        read_log(path, 123)
    with pytest.raises(FileNotFoundError):
        read_log("nonexistant-folder/", 0)


def test_build_database():
    path = "tests/test_reader/input/out_test/"
    name = "runinfo.parstud"

    num_lines = sum(1 for line in open(path+name)) - 1

    df = build_database(path, name)

    assert isinstance(df, pd.DataFrame)
    assert len(df.index) == num_lines

    bad_path = "nonexistant-folder/"
    bad_name = "nonexistant-name"

    with pytest.raises(FileNotFoundError):
        df = build_database(bad_path, bad_name)
        df = build_database(path, bad_name)
        df = build_database(bad_path, name)
