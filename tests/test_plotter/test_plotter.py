from parstud.plotter.plotter import error_plot
from parstud.plotter.plotter import reduce_df
from parstud.plotter.plotter import piechart_plot
import sys
import os
import pytest
import pandas as pd


def test_error_plot():
    path = "tests/test_plotter/input/"
    df = pd.read_csv(path + "logs.csv")
    ext = "pdf"

    bad_path = "nonexistant-folder/"
    bad_df = 123
    bad_ext = "abc"

    with pytest.raises(TypeError):
        error_plot(bad_df, path, ext)
        error_plot(df,bad_df,ext)
        error_plot(df, path, bad_df)
    with pytest.raises(FileNotFoundError):
        error_plot(df, bad_path, ext)
    with pytest.raises(ValueError):
        error_plot(df, path, bad_ext)


def test_reduce_df():
    path = "tests/test_plotter/input/"
    df = pd.read_csv(path + "logs.csv")
    df_r = reduce_df(df)

    assert isinstance(df, pd.DataFrame)

    bad_df = 123

    with pytest.raises(TypeError):
        df_r = reduce_df(bad_df)


def test_piechart_plot():
    path = "tests/test_plotter/input/"
    df = pd.read_csv(path + "logs.csv")
    ext = "pdf"

    bad_path = "nonexistant-folder/"
    bad_df = 123
    bad_ext = "abc"

    with pytest.raises(TypeError):
        piechart_plot(bad_df, path, ext)
    with pytest.raises(FileNotFoundError):
        piechart_plot(df, bad_path, ext)
    with pytest.raises(ValueError):
        piechart_plot(df, path, bad_ext)
