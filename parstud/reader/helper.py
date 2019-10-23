def read_log_list(dir):
    """
    Reads log files at given directory and returns relevant time data in list
    """
    data = []
    # Define strings which signal the function and the time
    str_func = '...'
    str_time = 'Done in '
    with open(dir, 'r') as reader:
        for line in reader:
            # If line includes the strings write function and time in data
            if str_func in line and str_time in line:
                # Extract function and time based on the strings above
                lin_func = line[0:line.find(str_func)]
                lin_time = line[line.find(str_time)+len(str_time):-3]
                # Append to list
                data.append([lin_func, lin_time])
    return data


def read_log_dict(dir):
    """
    Reads log files at given directory and returns relevant time data in dictionary
    """
    data = {'function': [], 'time': []}
    func = []
    time = []
    # Define strings which signal the function and the time
    str_func = '...'
    str_time = 'Done in '
    with open(dir, 'r') as reader:
        for line in reader:
            # If line includes the strings write function and time in data
            if str_func in line and str_time in line:
                # Extract function and time based on the strings above
                func.append(line[0:line.find(str_func)])
                time.append(float(line[line.find(str_time)+len(str_time):-3]))
    data = dict(zip(func, time))
    return data


def read_log_func(dir):
    """
    Reads log files at given directory and returns function data in list
    """
    func = []
    # Define string which signals the function
    str_func = '...'
    with open(dir, 'r') as reader:
        for line in reader:
            # If line includes the string, write function to list
            if str_func in line:
                # Extract function based on the strings above
                func.append(line[0:line.find(str_func)])
    return func


def read_log_time(dir):
    """
    Reads log files at given directory and time data in list
    """
    time = []
    with open(dir, 'r') as reader:
        for line in reader:
            # Define strings which signal the function and the time
            str_time = 'Done in '
            # If line includes the strings write function and time in data
            if str_time in line:
                # Extract function and time based on the strings above
                time.append(float(line[line.find(str_time)+len(str_time):-3]))
    return time


def read_log(dir, flag_is_time):
    """
    Reads log file at given directory and extracts either funtion as string list or time as float list


    Variables
    ---------
    dir:            directory where the log is located
    flag_is_time:   1 = return time data, 0 = return function data
    """
    return_list = []

    if flag_is_time == 1:
        str_t = 'Done in '
        with open(dir, 'r') as reader:
            for line in reader:
                if str_t in line:
                    return_list.append(
                        float(line[line.find(str_t)+len(str_t):-3]))
        return return_list
    elif flag_is_time == 0:
        str_f = '...'
        with open(dir, 'r') as reader:
            for line in reader:
                if str_f in line:
                    return_list.append(line[0:line.find(str_f)])
        return return_list
    else:
        print('Error: flag_is_time must be either 1 (time data) or 0 (function data)')


def get_log(pwd, fname, np):
    """
    Returns string for the 3DPOD log file for a given number of processors.


    Variables
    ---------
    pwd:    Path to log file from current working directory
    fname:  Name of the log file, excluding the number of processor used in run.
    np:     Number of processors.
    """
    log = pwd + fname + str(np)
    return log


def read_all_funcs(pwd, fname, np):
    """
    Returns list of strings for all function data in 3DPOD log files up to a given number of maximum processors.


    Variables
    ---------
    pwd:    Path to log file from current working directory
    fname:  Name of the log file, excluding the number of processor used in run.
    np:     Number of processors.
    """
    funcs = read_log(get_log(pwd, fname, np), 0)
    return funcs


def get_all_logs(pwd, fname, max_np):
    """
    Returns list of strings for all the 3DPOD log files up to a given number of maximum processors.


    Variables
    ---------
    pwd:    Path to log file from current working directory
    fname:  Name of the log file, excluding the number of processor used in run.
    max_np: Maximum number of processors.
    """
    logs = []
    for i in range(1, max_np+1):
        logs.append(get_log(pwd, fname, i))
    return logs


def read_all_times(pwd, fname, max_np):
    """
    Returns list of floats for all time data in 3DPOD log files up to a given number of maximum processors.


    Variables
    ---------
    pwd:    Path to log file from current working directory
    fname:  Name of the log file, excluding the number of processor used in run.
    max_np: Maximum number of processors.
    """
    times = []
    logs = get_all_logs(pwd, fname, max_np)
    for i in range(1, max_np+1):
        times.append(read_log(logs[i-1], 1))
    # Reashape times list of lists by transposing it
    times = list(map(list, zip(*times)))
    return times
