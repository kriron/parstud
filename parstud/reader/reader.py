import pandas as pd


def read_log(dir, flag_is_time):
    """
    Reads log file at given directory and extracts either funtion 
    as string list or time as float list.

    Parameters
    ----------
    dir             :   string    
        Path to log file including log file name.
    flag_is_time    :   int
        1 = return time data, 0 = return function data.

    Returns
    -------
    list
        With time or function data depending on flag_is_time.

    Raises
    ------
    TypeError
        If flag_is_time is not an integer.
    ValueError
        If flag_is_time is not either 0 nor 1.
    FileNotFoundError
        If dir does not exist.
    """
    return_list = []

    if not isinstance(flag_is_time, int):
        raise TypeError(
            "flag_is_time must be an integer (either 0 (for function data) or 1 (for time data) )"
        )
    else:
        if flag_is_time == 1:
            str_t = "Done in "
            with open(dir, "r") as reader:
                for line in reader:
                    if str_t in line:
                        return_list.append(
                            float(line[line.find(str_t) + len(str_t): -3]))
            return return_list
        elif flag_is_time == 0:
            str_f = "..."
            with open(dir, "r") as reader:
                for line in reader:
                    if str_f in line:
                        return_list.append(line[0: line.find(str_f)])
            return return_list
        else:
            raise ValueError(
                "flag_is_time must be either 0 (for function data) or 1 (for time data)"
            )


def build_database(path, name):
    """
    Returns returns database as dataFrame based on 3DPOD log files.

    Parameters
    ----------
    path    :   string    
        Path to log files
    name    :   string
        Name of the run info csv file

    Returns
    -------
    pandas.DataFrame
        With time and function data for all log files.

    Raises
    ------
    FileNotFoundError
        If path and or name do not exist.
    """

    info = pd.read_csv(path + name)

    nproc = info.command.str.split().str[-1]  # Number of processors
    fname = info.stdout_file  # File names
    npass = info.pass_no  # Pass number

    funcs = read_log(path + fname[1], 0)
    times = []

    for i in range(len(info.index)):
        times.append(read_log(path + fname[i], 1))

    df = pd.DataFrame(data=times, columns=funcs, index=fname)
    df["Number of processors"] = nproc.values
    df["Pass number"] = npass.values
    return df
