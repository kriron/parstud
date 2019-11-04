import os
import sys
import errno
import argparse
from runner.run_profile import *
from reader.reader import *


# execute_per_run_database(dbpath, rundb, dbfile):
# generate_syscalls(variations, cmd_string, env_var=False)
# run_and_gather_statistics(syscalls, datapath, passes_per_cmd=1, buildonly=False):


def run_study(args):
    # Check the desired output directory for existance and emptyness
    try:
        check_output_directory(args.dir, force=args.forcedir)
    except FileExistsError as _exc:
        parser.print_usage()
        print(_exc)
        sys.exit(errno.EEXIST)

    _syscalls = generate_syscalls(args.variations, args.systemcall)
    _passes = args.passes[0]
    run_and_gather_statistics(_syscalls, args.dir, _passes, buildonly=False)


def read_database_and_gather_data(args):
    if not os.path.isdir(args.idir):
        msg = "'{0!s}' is not an existing directory".format(args.idir)
        raise FileNotFoundError(msg)

    _dbf = os.path.join(args.idir, args.dbf)
    if not os.path.exists(_dbf):
        msg = "'{0!s}' does not exist".format(_dbf)
        raise FileNotFoundError(msg)

    if args.outf:
        if os.path.isfile(args.outf) and not os.access(args.outf, os.W_OK):
            msg = "Cannot write to {0!s}".format(args.outf)
            raise IOError(msg)

    _reader_df = build_database(args.idir, args.dbf)

    if args.outf:
        _reader_df.to_csv(args.outf)
    else:
        print(_reader_df)


def plot_logfile(args):
    raise NotImplementedError("Plotter not integrated yet.")


# ---

# Function for checking if a directory is valid.
def directory(dirstring):
    if os.path.isdir(dirstring) == False:
        msg = "'{0!s}' is not an existing directory".format(dirstring)
        raise argparse.ArgumentTypeError(msg)

    return dirstring


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
    # Create and configure an argument parser
    parser = argparse.ArgumentParser(
        description="""Script for performing parametric runs on system commands."""
    )

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="Commands for running, collecting and plotting data",
        help="Additional help",
    )

    # Add subparsers
    runner = subparsers.add_parser("run")
    runner.set_defaults(func=run_study)

    reader = subparsers.add_parser("read")
    reader.set_defaults(func=read_database_and_gather_data)

    plotter = subparsers.add_parser("plot")
    plotter.set_defaults(func=plot_logfile)

    # Configure the subparser for runner
    runner.add_argument("dir", help="""Directory where to store the run output.""")
    runner.add_argument(
        "-fd",
        "--forcedirectory",
        dest="forcedir",
        help="""Force usage of output directory. WARNING: This will wipe the specified drectory clean""",
        action="store_true",
    )
    runner.add_argument(
        "systemcall", help="""Base system call to be varied.""", type=str
    )
    runner.add_argument(
        "-v",
        "--variations",
        help="""Variations to be applied to base system call""",
        nargs="*",
        type=str,
        default=None,
    )
    runner.add_argument(
        "-p",
        "--passes",
        help="""Number of passes per systemcall variation.""",
        nargs=1,
        default=[1],
        type=int,
    )

    # Configure the subparser for reader
    reader.add_argument(
        "idir", help="""Directory where the databse and run output to read is stored."""
    )
    reader.add_argument(
        "-dbf",
        help="""Run database file name""",
        type=str,
        default="runinfo_parstud.csv",
    )
    reader.add_argument(
        "-o",
        help="""File to store the generated data in.""",
        type=str,
        dest="outf",
        default=None,
    )

    args = parser.parse_args()

    # Check if the parser returned a Namespace object without any content.
    # And if so, print the help.
    if not vars(args):
        parser.print_help()
        # Retrun invalid argument error code
        sys.exit(errno.EINVAL)

    # Execute the function associte with the subparser configured
    # above where the subparsers are added.
    args.func(args)
