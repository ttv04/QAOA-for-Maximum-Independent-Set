"""
Unit and regression test for the qaoamis package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

from ..qaoamis import *


def test_qaoamis_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "qaoamis" in sys.modules

mis = QAOAMIS()
