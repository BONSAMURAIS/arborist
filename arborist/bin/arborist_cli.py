#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Arborist CLI.

Usage:
  arborist-cli regenerate <dirpath>
  arborist-cli regenerate <dirpath> -i <input>

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
        generate_all(args["<dirpath>"], args["<input>"])
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
