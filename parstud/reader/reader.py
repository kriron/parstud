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
    elif flag_is_time == 0:
        str_f = "..."
        with open(dir, "r") as reader:
            for line in reader:
                if str_f in line:
                    return_list.append(line[0 : line.find(str_f)])
    else:
        print("Error: flag_is_time must be either 1 (time data) or 0 (function data)")
    return return_list


def build_database(path, name):
    """
    Returns returns database as dataFrame based on 3DPOD log files.

    Parameters
    ----------
    pwd     :   string    
        Path to log files
    name   :   string
        Name of the run info csv file
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


if __name__ == "__main__":
    name = "runinfo.parstud"
    path = "tests/input/run_test/out_1/"

    df = build_database(path, name)
    df.to_csv(path + "logs.csv")
