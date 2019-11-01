from parstud.reader.reader import build_database
from parstud.reader.reader import read_log
import sys
import os
import pytest
import pandas

sys.path.append(os.path.abspath("../parstud/"))


def test_template():
    with pytest.raises(TypeError):
        read_log("input/out_test/output.0", 123)
