import sys
import argparse
import os
import subprocess
import pprint
import pandas
import datetime


def is_os_compatible(osname):
    """
    Checks if the host OS is considered to be compatible with the script.

    Parameters
    ----------
    osname : string
        A string describing the host os. Can be generated with e.g. os.uname().

    Returns
    -------
    boolean
        True or False regarding OS compatibility.

    Raises
    ------
    TypeError
        If the input is not a string. 

    """

    # Check if osname is a string otherwise raise an error.
    if not isinstance(osname, str):
        raise TypeError("Input needs to be of type string")

    _osname = osname.lower()

    if 'linux' in _osname:
        return True
    
    else:
        return False


def generate_syscalls(variations, cmd_string, env_var=False):
    """
    Generates a list of systemcalls where variations are appended to cmd_string.
    If optional parameter env_var is defined, the variations are exported as
    an environment variable.

    Parameters
    ----------
    variations : list
        A list of strings containing the varaitions to append to cmd_string
    cmd_string : string
        The base command string
    env_var : string
        An environment variable to which the variation will be applied

    Returns
    -------
    list : 
        A list of strings which are to be used as systemcalls to run proceses.

    Example
    -------
    >>> generate_syscalls(['\"hello\"', '\"world\"'], 'echo ')
    ['echo  "hello"', 'echo  "world"']

    >>> generate_syscalls(['\"hello\"', '\"world\"'], "echo $WORLD_VAR", env_var="WORLD_VAR")
    ['export WORLD_VAR="hello" && echo $WORLD_VAR', 'export WORLD_VAR="world" && echo $WORLD_VAR']

    """
    _syscalls = []
    for _variation in variations:
        if env_var:
            _set_var_cmd = "export {0:s}={1} &&".format(env_var, _variation)
            _syscall = "{0:s} {1}".format(_set_var_cmd, cmd_string)
        else:
            _syscall = "{0:s} {1}".format(cmd_string, _variation)
        _syscalls.append(_syscall)
    return _syscalls


def run_stuff(syscall, use_shell=False):
    _cmd_out = subprocess.check_output(syscall, shell=use_shell)
    return _cmd_out


def prepare_run_database(syscalls, columnspec, passes_per_cmd=1):
    # Check if syscalls is a list or tuple.
    if not (isinstance(syscalls, list) or isinstance(syscalls, tuple)):
        raise TypeError("syscalls need to be of type list or tuple")

    if not isinstance(columnspec, list):
        raise TypeError("columnspec need to be of type list or tuple")

    _run_database = pandas.DataFrame(columns=columnspec)
    #_run_database = pandas.DataFrame()

    _dicts = []
    for _syscall in syscalls:
        for _i in range(1, passes_per_cmd+1):
            _dicts.append({'command': _syscall, 'pass no.': _i, \
                'desired passes': passes_per_cmd})

    _run_database = _run_database.append(pandas.DataFrame(_dicts))
    return _run_database


def execute_per_run_database(dbpath, rundb, dbfile):
    
    for _rundb_row in runbd.itertuples():
        # Check if command was run and reported as completed succesfully.
        # If true, skip and check next.
        if _rundb_row['attempted'] is True:
            break

        # Update the database with when command was started and print
        # update to file.
        rundb.at[_rundb_row.index, 'start time'] = \
            datetime.datetime.now().isoformat()
        rundb.to_csv(dbfile)

        # Run system command
        try:
            _cmd_out = subprocess.check_output(_rundb_row['command'], \
               stderr=subprocess.STDOUT)
            rundb.at[_rundb_row.index, 'exit status'] = 0
        except Exception as _exc:
            rundb.at[_rundb_row.index, 'exit status'] = _exc.returncode
            # _exc.output?
        finally:
            rundb.to_csv(dbfile)
            #with open(os.path.


        # Update the database with when command ended and print
        # update to file.
        rundb.at[_rundb_row.index, 'end time'] = \
            datetime.datetime.now().isoformat()
        #rundb.to_csv(dbfile)


def run_and_gather_statistics(syscalls, datapath, passes_per_cmd=1, \
        buildonly=False):
    # Implement:
    #  --> Takes a path as input for where to write files
    #  --> Take number of passes per command line as input
    #  --> Print os & machine information statistics to file
    #  --> Populate the database with successful run and desired passes
    #  --> Add column with exit status
    #  --> Name file names with e.g. <run no>.<desired run no>
    #  Put std err in file
    #  Put std out in file

    if not os.path.isdir(datapath):
        raise FileNotFoundError
    
    #
    # Add checking if the datapath is writable by script
    #

    #
    # Get CPU information
    # add a try-catch statement here
    _LSCPU = ["/usr/bin/lscpu"]
    if os.path.isfile(_LSCPU[0]) and os.access(_LSCPU[0], os.X_OK):
        _sys_info = os.fsdecode(subprocess.check_output(_LSCPU)) 
    else:
        # Implement optional method later
        _sys_info = None 

    _SYSINFOFILE = "sysinfo.parstud"
    with open(os.path.join(datapath, _SYSINFOFILE), mode='w') as f:
        f.write(_sys_info)
   
    #
    # Get memory information
    _FREE = ["/usr/bin/free", "--total", "--giga"]
    if os.path.isfile(_FREE[0]) and os.access(_FREE[0], os.X_OK):
        _mem_info = \
            os.fsdecode(subprocess.check_output(_FREE))
    else:
        # Implement optional method later 
        _mem_info = None 

    _MEMINFOFILE = "meminfo.parstud"
    with open(os.path.join(datapath, _MEMINFOFILE), mode='w') as f:
        f.write(_mem_info)


    #
    # Build database on run configuration and save to file
    _RUNSTATFILE = "runinfo.parstud"
    _df_columns = ['command', 'start time', 'end time', 
                   'stdout file', 'stderr file', 'exit status', 'pass no.', 
                   'desired passes', 'attempded'] 
    _rundb = prepare_run_database(syscalls, _df_columns, \
        passes_per_cmd=passes_per_cmd)
    _rundb.to_csv(os.path.join(datapath, _RUNSTATFILE))
        
    # If true then the execution step will be skipped
    if buildonly:
        return _rundb


if __name__ == "__main__":
    is_os_compatible(os.uname().sysname)

    print(
        'Number of physical CPUS on the system are {0}'.format(os.cpu_count())
    )
    print(
        os.uname()
    )
    
    no_threads = range(1,3)

    run_cmd = '../cppSource/3DPOD_u.out -i ./input -c output/chronos -m output/mode -p 381600 -v 3 -nm 200 -s 200 -np'

    calls = generate_syscalls(no_threads, run_cmd)
    for call in calls:
        print(call)

    run_stuff(["ls"])

    print('Done')


    #
    # Create and configure an argument parser
    #
    #parser = argparse.ArgumentParser(
    #    description = '''Script for performing profiling of the 3DPOD code.''')
    # parser.add_argument('-d', '--dir', 
    #     help = '''Directory containting the time directories.''',
    #     type = post_processing_dir,
    #     required = True)
    # parser.add_argument('-f', '--file',
    #     help = '''Name of VTK file to sample data from. Need to reside
    #     in the individual time directories.''',
    #     required = True)
    # parser.add_argument('-a', '--array',
    #     help = '''Name of the array to retrieve from the VTK file.''',
    #     required = True)
    # parser.add_argument('-o', '--out',
    #     help = '''File to store the output from the averaging proces''',
    #     required = True)
    #parser.add_argument('-r', '--radii',
    #    help = '''Define the sampling as <inner radius> <outer radius>''',
    #    nargs = 2,
    #    type = float,
    #    required = True)

