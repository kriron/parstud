import sys
import os
import shutil
import pytest
import pandas
import numpy as np
import pprint

#sys.path.append(os.path.abspath("../parstud/"))
from parstud.runner.run_profile import *


def presistent_relative_dir_helper(base_dir):
    _testrun = 1
    _max = 100
    while _testrun < _max:
        _output_dir = os.path.join(base_dir, "output/testrun_{0}".format(_testrun))
        # Added the absolute path check since, according to the documentation,
        # os.makedirs() can get confused by relative paths
        if not os.path.isabs(_output_dir):
            _output_dir = os.path.abspath(_output_dir)

        # Ensure empty output directory
        if os.path.isdir(_output_dir):
            shutil.rmtree(_output_dir)
        os.makedirs(_output_dir)

        yield _output_dir
        _testrun = _testrun + 1


def test_is_os_compatible():
    assert is_os_compatible("linux") == True
    assert is_os_compatible("Linux") == True
    assert is_os_compatible("Linux2") == True
    assert is_os_compatible("Windows") == False

    with pytest.raises(TypeError):
        is_os_compatible(123)


def test_generate_syscalls_parvar():
    # Assume that the there is a parameter that changes the
    # number of threads to use.
    _out = generate_syscalls([1, 2, 3], "cmd -np")
    assert _out == ["cmd -np 1", "cmd -np 2", "cmd -np 3"]


def test_generate_syscalls_envvar():
    # Generate a syscall that sets an environment variable.
    _out = generate_syscalls([1, 2, 3], "cmd_to_run test", env_var="PAR_RUNS")
    assert _out == [
        "export PAR_RUNS=1 && cmd_to_run test",
        "export PAR_RUNS=2 && cmd_to_run test",
        "export PAR_RUNS=3 && cmd_to_run test",
    ]


def test_generate_syscalls_novar():
    # Assume that there are no variations specified
    _out = generate_syscalls(None, "cmd -np")
    assert _out == ["cmd -np"]


def test_run_stuff_lsexistdir():
    _curr_path_file = os.path.realpath(__file__)
    _curr_dir = os.path.dirname(_curr_path_file)

    # The output stream generated by ls needs to be encoded or decoded
    # according to the file system rules. This can be achieved in
    # python using os.fsencode() and os.fsdecode().
    _test_ls_path = os.path.join(_curr_dir, "input/ls_test/")
    _ls_out = run_stuff("ls {path}".format(path=_test_ls_path).split())
    assert _ls_out == os.fsencode("file1.txt\nfile_2.txt\nwierd_file.txt\n")
    assert os.fsdecode(_ls_out) == "file1.txt\nfile_2.txt\nwierd_file.txt\n"


def test_run_stuff_echoenv():
    # Check setting environment variables
    _env_out = run_stuff(["export MY_ENV='hello 2' && echo $MY_ENV"], use_shell=True)
    assert _env_out == b"hello 2\n"
    assert os.fsdecode(_env_out) == os.fsdecode(b"hello 2\n")


def test_prepare_run_database():
    _rundatabase = prepare_run_database(
        ["cmd1", "cmd2"], columnspec=["column1", "column2"]
    )

    # Configure database to compare with
    _df = pandas.DataFrame(columns=["column1", "column2"])
    _df = _df.append(
        pandas.DataFrame(
            [
                {"command": "cmd1", "desired_passes": 1.0, "pass_no": 1.0},
                {"command": "cmd2", "desired_passes": 1.0, "pass_no": 1.0},
            ]
        ),
        sort=True,
    )

    # Use Pandas built-in functionality to perform comparison of dataframes
    pandas.util.testing.assert_frame_equal(_rundatabase, _df)


def test_prepare_run_database_typeerr():
    with pytest.raises(TypeError):
        prepare_run_database("cmd", columnspec=["column1", "column2"])


def test_run_and_gather_statistics():
    _curr_path_file = os.path.realpath(__file__)
    _curr_dir = os.path.dirname(_curr_path_file)

    _output_dir_iter = iter(presistent_relative_dir_helper(_curr_dir))
    pprint.pprint("")

    # Run a simple command with existing output dir.
    # No execution since buildonly is set to true
    _output_dir = next(_output_dir_iter)
    pprint.pprint("Using directory: {}".format(_output_dir))
    run_and_gather_statistics(["cmd"], _output_dir, buildonly=True)

    # Run a simple command with non-existant output dir
    _err_output_dir = os.path.join(_curr_dir, "output/testrun-nonexist")
    with pytest.raises(FileNotFoundError):
        run_and_gather_statistics(["cmd"], _err_output_dir, buildonly=True)

    # Generate syscalls and build run database
    # No execution since buildonly is set to true
    _variations = [1, 2, 3, 4, 5]
    _basecmd = "par run -np"
    _syscalls = generate_syscalls(_variations, _basecmd)
    _passes_per_cmd = 3
    _output_dir = next(_output_dir_iter)
    pprint.pprint("Using directory: {}".format(_output_dir))
    run_and_gather_statistics(
        _syscalls, _output_dir, passes_per_cmd=_passes_per_cmd, buildonly=True
    )

    # Generate syscalls, build run database and execute commands
    _variations = [".", "blargh"]
    _basecmd = "/bin/ls"  # Could also be in "/usr/bin/ls"
    _syscalls = generate_syscalls(_variations, _basecmd)
    _passes_per_cmd = 1
    _output_dir = next(_output_dir_iter)
    pprint.pprint("Using directory: {}".format(_output_dir))
    run_and_gather_statistics(_syscalls, _output_dir, passes_per_cmd=_passes_per_cmd)
