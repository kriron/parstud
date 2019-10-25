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
        type=directory,
        required=True,
    )
    parser.add_argument(
        "-s", "--systemcall", help="""Base system call to be varied.""", type=str
    )
    parser.add_argument(
        "-v",
        "--variations",
        help="""Variations to be applied to base system call""",
        nargs="*",
        type=str,
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
    run_study(args)