import os
import subprocess
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

    if "linux" in _osname:
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
    variations : list or None
        A list of strings containing the varaitions to append to cmd_string
    cmd_string : string
        The base command string
    env_var : string, optional
        An environment variable to which the variation will be applied

    Returns
    -------
    list :
        A list of strings which are to be used as systemcalls to run proceses.
        
    Raises
    ------
    TypeError
        If the input is of wrong type.

    Example
    -------
    >>> generate_syscalls(['\"hello\"', '\"world\"'], 'echo ')
    ['echo  "hello"', 'echo  "world"']

    >>> generate_syscalls(['\"hello\"', '\"world\"'],
                          "echo $WORLD_VAR",
                          env_var="WORLD_VAR")
    ['export WORLD_VAR="hello" && echo $WORLD_VAR', 'export WORLD_VAR="world" && echo $WORLD_VAR']
    """

    # Check if cmd_string is a string otherwise raise an error.
    if not isinstance(cmd_string, str):
        raise TypeError("cmd_string needs to be of type string")

    # Check if variations is not None, if so if it is a list or tuple.
    if not (
        variations == None
        or isinstance(variations, list)
        or isinstance(variations, tuple)
    ):
        raise TypeError("variations need to be either 'None' or of type list or tuple")

    # Check if env_var is set and is a string otherwise raise an error.
    if env_var and not isinstance(env_var, str):
        raise TypeError("env_var needs to be of type string")

    _syscalls = []

    # If no variation is specified, just returns the cmd_string as a
    # one-element list
    if variations == None:
        _syscalls.append(cmd_string)

    else:
        for _variation in variations:
            if env_var:
                _set_var_cmd = "export {0:s}={1} &&".format(env_var, _variation)
                _syscall = "{0:s} {1}".format(_set_var_cmd, cmd_string)
            else:
                _syscall = "{0:s} {1}".format(cmd_string, _variation)
            _syscalls.append(_syscall)

    return _syscalls


def run_stuff(syscall, use_shell=False):
    """
    Simple wrapper for subprocess.check_output. Mainly used for testing.

    Returns
    -------
    string
    """

    _cmd_out = subprocess.check_output(syscall, shell=use_shell)
    return _cmd_out


def prepare_run_database(syscalls, columnspec=False, passes_per_cmd=1):
    """
    This function can be used to populate a pandas dataFrame object with
    data to run parameteric studies on system calls. Used internally in this
    module to achieve just that.

    Parameters
    ----------
    syscalls : list or tuple
        list of systemcalls used for populating the run database.

    columnspec : list or tuple, optional
        list to use as column specifier for the run database.

    passes_per_cmd : int, optional
        speciefier on how many times each syscall is going to be executed.

    Returns
    -------
    pandas.dataFrame
        A populated pandas.dataFrame object

    Raises
    ------
    TypeError
        If the input is of wrong type.

    Example
    -------

    # Example 1

    >>> df = prepare_run_database(["cmd1", "cmd2", "cmd3"], passes_per_cmd=2)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    # Example 2

    >>> prepare_run_database(["cmd1", "cmd2", "cmd3"], passes_per_cmd=2)
      command  desired_passes  pass_no
    0    cmd1               2        1
    1    cmd1               2        2
    2    cmd2               2        1
    3    cmd2               2        2
    4    cmd3               2        1
    5    cmd3               2        2

    # Example 3

    >>> prepare_run_database(["cmd1", "cmd2", "cmd3"], 
                             columnspec=["cmdinfo1", "cmdinfo2"],
                             passes_per_cmd=2)
      cmdinfo1 cmdinfo2 command  desired_passes  pass_no
    0      NaN      NaN    cmd1             2.0      1.0
    1      NaN      NaN    cmd1             2.0      2.0
    2      NaN      NaN    cmd2             2.0      1.0
    3      NaN      NaN    cmd2             2.0      2.0
    4      NaN      NaN    cmd3             2.0      1.0
    5      NaN      NaN    cmd3             2.0      2.0

    """

    # Check if syscalls is a list or tuple.
    if not (isinstance(syscalls, list) or isinstance(syscalls, tuple)):
        raise TypeError("syscalls need to be of type list or tuple")

    if columnspec and not (isinstance(syscalls, list) or isinstance(syscalls, tuple)):
        raise TypeError("columnspec needs to be of type string")

    if not (isinstance(passes_per_cmd, int) or passes_per_cmd < 1):
        raise TypeError("passes_per_cmd need to be of type int and 1 or larger")

    if columnspec:
        _run_database = pandas.DataFrame(columns=columnspec)
    else:
        _run_database = pandas.DataFrame()

    _dicts = []
    for _syscall in syscalls:
        for _i in range(1, passes_per_cmd + 1):
            _dicts.append(
                {"command": _syscall, "pass_no": _i, "desired_passes": passes_per_cmd}
            )

    _run_database = _run_database.append(pandas.DataFrame(_dicts), sort=True)
    return _run_database


def execute_per_run_database(dbpath, rundb, dbfile):
    """
    Takes a pandas dataFrame object and executes what is liste in the 'commands'
    column as system calls. Writes the command outputs to persistent storage in
    for later digestion.

    A suitable run database can be generated with the `prepare_run_database`
    function.
    
    Parameters
    ----------
    dbpath : string
        path to location on peristent storage where the run database is stored
    
    rundb : pandas.dataFrame
        pandas dataFrame object containning the run configuration
        
    dbfile : string
        name of the file where the rundb dataFrame is written to 
        (located in dbpath)

    Returns
    -------
    Nothing
    
    Raises
    ------
    Nothing

    """

    _DBFILE = os.path.join(dbpath, dbfile)

    for _rundb_row in rundb.itertuples():
        # Check if command was run and reported as attempted.
        # If true, skip and check next. _rundb_row is a named tuple, hence
        # the existance of the keyword 'attempeted' is assessed by retrieveing
        # the list of fields in the named tuple.
        if ("attempted" in _rundb_row._fields) and (_rundb_row.attempted is True):
            continue

        # Update the database with when command was started and print
        # update to file.
        rundb.at[_rundb_row.Index, "start_time"] = datetime.datetime.now().isoformat()
        rundb.to_csv(_DBFILE)

        # Run system command
        _cmd_out = ""
        try:
            # Run the command
            _cmd_out = subprocess.check_output(
                _rundb_row.command.split(), stderr=subprocess.STDOUT
            )
            # If no exception indicate succesful run in database
            rundb.at[_rundb_row.Index, "exit_status"] = 0
        except subprocess.CalledProcessError as _exc:
            # If unsuccessful execution store the returnceode in database
            rundb.at[_rundb_row.Index, "exit_status"] = _exc.returncode
            # Retrieve the error output from the exception
            _cmd_out = _exc.output
        except Exception as _exc:
            raise _exc
        finally:
            # Indicate that the command was attempted in database
            rundb.at[_rundb_row.Index, "attempted"] = True
            rundb.to_csv(_DBFILE)

            # Write output to file
            _CMDOUTFILE = "output_{0}.txt".format(_rundb_row.Index)
            with open(os.path.join(dbpath, _CMDOUTFILE), mode="w") as f:
                f.write(os.fsdecode(_cmd_out))
            rundb.at[_rundb_row.Index, "stdout_file"] = _CMDOUTFILE
            rundb.to_csv(_DBFILE)

        # Update the database with when command ended and print
        # update to file.
        rundb.at[_rundb_row.Index, "end_time"] = datetime.datetime.now().isoformat()
        rundb.to_csv(_DBFILE)


def run_and_gather_statistics(syscalls, datapath, passes_per_cmd=1, buildonly=False):
    """
    Function that will configure a run database and execute the system calls of
    the database. Will store system information in the folder specified by
    datapath together with the run database.

    If buildonly=True, will return the generated run database as a pandas
    DataFrame object and skip execution.

    Parameters
    ----------
    syscalls : list or tuple
        list of systemcalls used for populating the run database.

    dbpath : string
        path to location on peristent storage where the run database is stored

    passes_per_cmd : int, optional
        speciefier on how many times each syscall is going to be executed.

    buildonly : boolean, optional
        dictates if all system commands will be run after gathering system
        information and construction of run database. Default is False.

    Returns
    -------
    pandas.DataFrame
        When buildonly=True, otherwise nothing.

    Raises
    ------
    FileNotFoundError
        If dbpath does not exist.
    """

    if not os.path.isdir(datapath):
        raise FileNotFoundError

    #
    # Add checking if the datapath is writable by script
    #

    # Get CPU information
    # add a try-catch statement here
    _LSCPU = ["/usr/bin/lscpu"]
    if os.path.isfile(_LSCPU[0]) and os.access(_LSCPU[0], os.X_OK):
        _sys_info = os.fsdecode(subprocess.check_output(_LSCPU))
    else:
        # Implement optional method later
        _sys_info = None

    _SYSINFOFILE = "sysinfo_parstud.txt"
    with open(os.path.join(datapath, _SYSINFOFILE), mode="w") as f:
        f.write(_sys_info)

    # Get memory information
    _FREE = ["/usr/bin/free", "--total", "--giga"]
    if os.path.isfile(_FREE[0]) and os.access(_FREE[0], os.X_OK):
        _mem_info = os.fsdecode(subprocess.check_output(_FREE))
    else:
        # Implement optional method later
        _mem_info = None

    _MEMINFOFILE = "meminfo_parstud.txt"
    with open(os.path.join(datapath, _MEMINFOFILE), mode="w") as f:
        f.write(_mem_info)

    # Build database on run configuration and save to file
    _RUNSTATFILE = "runinfo_parstud.csv"
    _rundb = prepare_run_database(syscalls, passes_per_cmd=passes_per_cmd)
    _rundb.to_csv(os.path.join(datapath, _RUNSTATFILE))

    # If true then the execution step will be skipped
    if buildonly:
        return _rundb

    # Run commands
    execute_per_run_database(datapath, _rundb, _RUNSTATFILE)
