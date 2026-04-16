"""
Unit and regression test for the qaoamis package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import qaoamis

mis = qaoamis.QAOAMIS()

def test_qaoamis_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "qaoamis" in sys.modules

def test_qaoamis_class():
    """Test the QAOAMIS class."""
    assert isinstance(mis, qaoamis.QAOAMIS)

def test_exceptions():
    """Test that exceptions are raised when expected."""
    with pytest.raises(ValueError):
        mis.mis_brute_force()
    with pytest.raises(ValueError):
        mis.buildCostHamiltonian()
    with pytest.raises(ValueError):
        mis.buildQAOAAnsatz()
    with pytest.raises(ValueError):
        mis.buildQUBO()
    with pytest.raises(ValueError):
        mis.buildCostHamiltonian()
    with pytest.raises(ValueError):
        mis.find_optimal_parameters()

