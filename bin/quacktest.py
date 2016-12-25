#!/usr/bin/python

import argparse
import sys

from QuackTest import core


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="The Ducky Script to execute")
    parser.add_argument("-e", "--exit-on-error", help="Runs the script and exit on any errors. "
                                                      "(Otherwise the script will continue to try to run)",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="Set logging to debug mode", action="store_const", const="DEBUG",
                        default="INFO")

    return parser.parse_args()


def main():
    args = parse_args()
    quack_tester = core.QuackTester()

    try:
        file = open(args.script)
        lines = file.readlines()
        quack_tester.run(lines, soft_errors=not args.exit_on_error, log_level=args.verbose)
    except FileNotFoundError:
        print("Cannot open script at " + args.script + ". Aborting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
