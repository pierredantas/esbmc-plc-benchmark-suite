#!/usr/bin/env python3
"""One spelling rule for paths that end up inside a published record.

A record is read by people who do not have the machine that produced it. An absolute
path neither runs there nor tells them anything they can use, and it publishes a
directory layout that was never part of the result.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def portable(arg):
    """Repo-relative inside the suite, ~ under home, unchanged elsewhere."""
    if not isinstance(arg, str):
        return arg
    if arg == ROOT or arg.startswith(ROOT + os.sep):
        return os.path.relpath(arg, ROOT)
    home = os.path.expanduser("~")
    if arg.startswith(home + os.sep):
        return "~" + arg[len(home):]
    return arg
