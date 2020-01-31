"""Misc helper functions"""

from contextlib import contextmanager
import sys
import os


@contextmanager
def suppress_stdout():
    """Supresses stdout in context

    Kudos to Dave Smith: http://thesmithfam.org/blog/2012/10/25/
    temporarily-suppress-console-output-in-python/
    """
    with open(os.devnull, "w") as devnull:
        tmp_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = tmp_stdout
