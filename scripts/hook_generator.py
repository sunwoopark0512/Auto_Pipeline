"""Wrapper script to run :mod:`hook_generator` from the ``scripts`` directory."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # pylint: disable=wrong-import-position

from hook_generator import generate_hooks  # type: ignore

if __name__ == "__main__":
    generate_hooks()
