if __name__== "__main__":
    import helper
else:
    from . import helper

import pandas as pd

# ------ User input ------
# Path to log files
pwd = '../tests/input/logs_test/'
# Name of the log files, excluding number of cores
fname = 'log.run_np_'
# Number of cores
max_np = 4
# ------------------------

df = helper.build_database(pwd,fname,max_np)

df.to_csv(pwd+'logs.csv')

print(df)