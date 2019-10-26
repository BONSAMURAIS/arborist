#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Arborist CLI.

Usage:
  arborist-cli regenerate <dirpath>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from arborist import generate_all
import sys


def main():
    try:
        args = docopt(__doc__, version="0.2")
        generate_all(args["<dirpath>"])
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
