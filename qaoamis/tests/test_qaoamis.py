"""
Unit and regression test for the qaoamis package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import qaoamis


def test_qaoamis_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "qaoamis" in sys.modules

def test_qaoamis_class():
    """Test the QAOAMIS class."""
    mis = qaoamis.QAOAMIS()
    assert isinstance(mis, qaoamis.QAOAMIS)
