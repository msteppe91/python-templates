#!/usr/bin/env python3
"""
Template class for argparse method
"""

import argparse
import sys


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
    required = parser.add_argument_group('required arguments')
    # Re-add optional args to parser now that required args exist
    parser._action_groups.append(optional)  # pylint: disable=protected-access

    # Required positional arguments
    parser.add_argument("number",
                        type=int,
                        help="display the given integer raised to a power provided by -p flag")

    # Required arguments
    required.add_argument("-p", "--power",
                          type=int,
                          help="The first required arg",
                          required=True)

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
    print(f"{args.number} ** {args.power} = {args.number ** args.power}")

    raise SystemExit(0)


# This is executed when run from the command line
if __name__ == "__main__":
    main()
