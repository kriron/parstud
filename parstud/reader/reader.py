import helper as hp
import pandas as pd

pwd = 'tests/input/logs_test/'
fname = 'log.run_np_'
max_np = 4

funcs = hp.read_all_funcs(pwd, fname, max_np)
times = hp.read_all_times(pwd, fname, max_np)
rlogs = hp.get_all_logs(pwd, fname, max_np)
r_idx = [item.replace(pwd+fname[0:4], '') for item in rlogs]
r_dat = dict(zip(funcs, times))

df = pd.DataFrame(data=r_dat, index=r_idx)

df.to_csv(pwd+'logs.csv')

print(df)