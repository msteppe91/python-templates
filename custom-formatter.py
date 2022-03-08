#!/usr/bin/env python3
"""
Template class for custom logging formatter to colorize logging output
"""

import argparse
import logging
import os
import sys


class CustomFormatter(logging.Formatter):
    """
    Custom formatting class that allows our log messages to be shorter and colored based on level
    """
    cyan = "\x1b[36;20m"
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Pick ONE formatter from below
    # Simple logger format (contains level and timestamp)
    formatter = "[%(levelname).4s %(asctime).19s] %(message)s"
    # More verbose logger format (contains level, timestamp, script name, and line number)
    verbose_formatter = "[%(levelname).1s %(asctime).19s %(filename)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + formatter + reset,
        logging.INFO: cyan + formatter + reset,
        logging.WARNING: yellow + formatter + reset,
        logging.ERROR: red + formatter + reset,
        logging.CRITICAL: bold_red + formatter + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        my_formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return my_formatter.format(record)


def setup_logger(args: argparse.Namespace) -> logging.Logger:
    """
    Sets up logger object

    Args:
        args (argparse.Namespace) - The argparse object that contains the list of parsed arguments
    Returns:
        logging.Logger - logger object to use in this module
    """
    # Setup custom logger for colorized output
    logger = logging.getLogger(__name__)
    log_level = logging.DEBUG if args.verbose >= 1 else logging.INFO
    logger.setLevel(log_level)

    # Stream handler (console / stdout)
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(CustomFormatter())
    logger.addHandler(stream)

    # Append to file by default (change to 'w' to overwrite)
    file = logging.FileHandler("out.log", mode="a")
    fileformat = logging.Formatter(
        "[%(levelname).4s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S")
    file.setLevel(log_level)
    file.setFormatter(fileformat)
    logger.addHandler(file)

    return logger


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

    # Setup logger
    logger = setup_logger(args)

    # Do work
    logger.debug("Hello World")
    logger.info("Hello World")
    logger.warning("Hello World")
    logger.error("Hello World")
    logger.critical("Hello World")

    raise SystemExit(0)


# This is executed when run from the command line
if __name__ == "__main__":
    main()
