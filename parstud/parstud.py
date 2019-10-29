import sys
import errno
import argparse
from runner.run_profile import *


# execute_per_run_database(dbpath, rundb, dbfile):
# generate_syscalls(variations, cmd_string, env_var=False)
# run_and_gather_statistics(syscalls, datapath, passes_per_cmd=1, buildonly=False):


def run_study(args):
    _syscalls = generate_syscalls(args.variations, args.systemcall)
    _passes = args.passes[0]
    run_and_gather_statistics(_syscalls, args.dir, _passes, buildonly=False)


# ---

# Function for checking if a directory is valid.
def directory(string):
    if os.path.isdir(string) == False:
        msg = "'{0!s}' is not an existing directory".format(string)
        raise argparse.ArgumentTypeError(msg)
    return string


# Function for checking, creating and/or cleaning the desired output dir.
def check_output_directory(dirstring, force=False):
    if os.path.isdir(dirstring) == False:
        msg = "Creating output directory '{0!s}'".format(dirstring)
        # print(msg)
        os.makedirs(dirstring)

    if os.path.isdir(dirstring) == True and not os.listdir(dirstring):
        msg = "Using empty directory '{0!s}' for output".format(dirstring)
        # print(msg)

    if os.path.isdir(dirstring) == True and os.listdir(dirstring):
        msg = "Directory '{0!s}' is not empty".format(dirstring)
        # print(msg)

        if force:
            msg = "Forcing use of {0!s}! Cleaning directory...".format(dirstring)
            # print(msg)
            for _file in os.listdir(dirstring):
                os.remove(os.path.join(dirstring, _file))

        if not force:
            msg = "Directory {0!s} is not empty.\n    Add flag -fd/--forcedirectory to force cleaning and usage of directory".format(
                dirstring
            )
            raise FileExistsError(msg)

    return dirstring


if __name__ == "__main__":
    print("This is currently work in progress. Check back later.")

    # Create and configure an argument parser
    parser = argparse.ArgumentParser(
        description="""Script for performing parametric runs on system commands."""
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="""Directory where to store the run output.""",
        # type=directory,
        required=True,
    )
    parser.add_argument(
        "-fd",
        "--forcedirectory",
        dest="forcedir",
        help="""Force usage of output directory. WARNING: This will wipe the specified drectory clean""",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--systemcall",
        help="""Base system call to be varied.""",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-v",
        "--variations",
        help="""Variations to be applied to base system call""",
        nargs="*",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-p",
        "--passes",
        help="""Number of passes per systemcall variation.""",
        nargs=1,
        default=[1],
        type=int,
    )

    args = parser.parse_args()

    # Check the desired output directory for existance and emptyness
    try:
        check_output_directory(args.dir, force=args.forcedir)
    except FileExistsError as _exc:
        parser.print_usage()
        print(_exc)
        sys.exit(errno.EEXIST)

    run_study(args)
