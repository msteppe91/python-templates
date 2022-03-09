#!/usr/bin/env python3
"""
Template class for subprocess.Popen() method
"""

import argparse
import sys
import subprocess


def run_cmd(cmd: str) -> str:
    """
    Runs command with subprocess.Popen() and returns stdout or prints to stderr

    Args:
        cmd (str) - the command string to run via python subprocess.Popen and "sh -c"
    Returns:
        str - the returned output string of the command we just ran
    """
    try:
        with subprocess.Popen(["sh", "-c", cmd],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True) as cmd_proc:
            cmd_out, cmd_err = cmd_proc.communicate()
            # Debugging lines
            #print(f"cmd stdout:\n{cmd_out}")
            #print(f"cmd stderr:\n{cmd_err}")
        if cmd_proc.returncode != 0:
            print(f"Failed to run cmd '{cmd}'. See error below:\n\n{cmd_err}", file=sys.stderr)
            raise SystemExit(1)
        return cmd_out.strip()
    except IOError as err:
        print("Caught IO exception. Exiting now as we likely didn't do something correctly. "
              f"See error below:\n\n{err}", file=sys.stderr)
        raise SystemExit(1) from err


def read_command_line_arguments(passed_arguments: list) -> argparse.Namespace:
    """
    Parses command line arguments passed to this script

    Args:
        passed_arguments (list) - e.g. command line arg list (sys.argv[1:])
    Returns:
        argparse.Namespace - argparse object containing parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__)
    # Pop optional args off parser to get required first in help documentation
    optional = parser._action_groups.pop()  # pylint: disable=protected-access
    # required = parser.add_argument_group('required arguments')
    # Re-add optional args to parser now that required args exist
    parser._action_groups.append(optional)  # pylint: disable=protected-access

    # Required positional arguments
    parser.add_argument("package",
                        type=str,
                        help="display the 'rpm -qa | grep <package>' output")

    # Required arguments

    # Optional arguments
    optional.add_argument("-v", "--verbose",
                          action="count",
                          default=0,
                          help="Verbosity (-v, -vv, etc)")

    args = parser.parse_args(passed_arguments)
    return args


def main():
    """
    Main method
    """
    # Parse cmd line args
    args = read_command_line_arguments(sys.argv[1:])

    # Do work
    print(args)
    print(run_cmd(f"rpm -qa | grep {args.package} | sort"))

    raise SystemExit(0)


# This is executed when run from the command line
if __name__ == "__main__":
    main()
