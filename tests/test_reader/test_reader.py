# -*- coding: utf-8 -*-
import pprint
import os
import shutil

from parstud.reader.reader import *

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


def test_execute_reader():
    _curr_path_file = os.path.realpath(__file__)
    _curr_dir = os.path.dirname(_curr_path_file)
    _output_dir_iter = iter(presistent_relative_dir_helper(_curr_dir))
    
    
    # Run reader 
    _output_dir = next(_output_dir_iter)
    _input_path = os.path.join(_curr_dir, "input/out_1/")
    _rundb_fname = "runinfo.parstud"
    _rundb_df = build_database(_input_path, _rundb_fname)
    _rundb_df.to_csv(os.path.join(_output_dir,"logs.csv"))
    pprint.pprint(_rundb_df)
    
    