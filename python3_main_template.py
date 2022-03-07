#!/usr/bin/env python3
"""
A simple python3 template with just a main function.
"""

import sys
import argparse


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,  # this evaluates to the module doc string
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))

    args = parser.parse_args(arguments)

    print(args)


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
