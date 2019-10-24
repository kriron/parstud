import pandas as pd


def read_log(dir, flag_is_time):
    """
    Reads log file at given directory and extracts either funtion as string list or time as float list

    Parameters
    ----------
    dir             :   string    
        Path to log file from current working directory
    flag_is_time    :   bool
        1 = return time data, 0 = return function data
    """
    return_list = []

    if flag_is_time == 1:
        str_t = "Done in "
        with open(dir, "r") as reader:
            for line in reader:
                if str_t in line:
                    return_list.append(float(line[line.find(str_t) + len(str_t) : -3]))
        return return_list
    elif flag_is_time == 0:
        str_f = "..."
        with open(dir, "r") as reader:
            for line in reader:
                if str_f in line:
                    return_list.append(line[0 : line.find(str_f)])
        return return_list
    else:
        print("Error: flag_is_time must be either 1 (time data) or 0 (function data)")


def get_log(pwd, fname, np):
    """
    Returns string for the 3DPOD log file for a given number of processors.

    Parameters
    ----------
    pwd     :   string    
        Path to log file from current working directory
    fname   :   string
        Name of the log file, excluding the number of processor used in run.
    np      :   int
        Number of processors.
    """
    log = pwd + fname + str(np)
    return log


def read_all_funcs(pwd, fname, np):
    """
    Returns list of strings for all function data in 3DPOD log files up to a given number of maximum processors.

    Parameters
    ----------
    pwd     :   string    
        Path to log file from current working directory
    fname   :   string
        Name of the log file, excluding the number of processor used in run.
    np      :   int
        Number of processors.
    """
    funcs = read_log(get_log(pwd, fname, np), 0)
    return funcs


def get_all_logs(pwd, fname, max_np):
    """
    Returns list of strings for all the 3DPOD log files up to a given number of maximum processors.

    Parameters
    ----------
    pwd     :   string    
        Path to log file from current working directory
    fname   :   string
        Name of the log file, excluding the number of processor used in run.
    max_np  :   int
        Maximum number of processors.
    """
    logs = []
    for i in range(1, max_np + 1):
        logs.append(get_log(pwd, fname, i))
    return logs


def read_all_times(pwd, fname, max_np):
    """
    Returns list of floats for all time data in 3DPOD log files up to a given number of maximum processors.

    Parameters
    ----------
    pwd     :   string    
        Path to log file from current working directory
    fname   :   string
        Name of the log file, excluding the number of processor used in run.
    max_np  :   int
        Maximum number of processors.
    """
    times = []
    logs = get_all_logs(pwd, fname, max_np)
    for i in range(1, max_np + 1):
        times.append(read_log(logs[i - 1], 1))
    # Reashape times list of lists by transposing it
    times = list(map(list, zip(*times)))
    return times


def build_database(pwd, fname, max_np):
    """
    Returns returns database as dataFrame based on 3DPOD log files up to a given number of maximum processors.

    Parameters
    ----------
    pwd     :   string    
        Path to log file from current working directory
    fname   :   string
        Name of the log file, excluding the number of processor used in run.
    max_np  :   int
        Maximum number of processors.
    """
    funcs = read_all_funcs(pwd, fname, max_np)
    times = read_all_times(pwd, fname, max_np)
    rlogs = get_all_logs(pwd, fname, max_np)
    r_idx = [item.replace(pwd + fname[0:4], "") for item in rlogs]
    r_dat = dict(zip(funcs, times))
    df = pd.DataFrame(data=r_dat, index=r_idx)
    return df
