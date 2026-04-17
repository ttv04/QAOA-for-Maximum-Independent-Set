"""
Unit and regression test for the qaoamis package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest
from unittest.mock import patch
from matplotlib import pyplot as plt

import qaoamis

mis_error = qaoamis.QAOAMIS()
mis = qaoamis.QAOAMIS()

def test_qaoamis_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "qaoamis" in sys.modules

def test_qaoamis_class():
    """Test the QAOAMIS class."""
    assert isinstance(mis_error, qaoamis.QAOAMIS)
    assert isinstance(mis, qaoamis.QAOAMIS)

def test_exceptions():
    """Test that exceptions are raised when expected."""
    with pytest.raises(ValueError):
        mis_error.mis_brute_force()
    with pytest.raises(ValueError):
        mis_error.buildCostHamiltonian()
    with pytest.raises(ValueError):
        mis_error.buildQAOAAnsatz()
    with pytest.raises(ValueError):
        mis_error.buildQUBO()
    with pytest.raises(ValueError):
        mis_error.buildCostHamiltonian()
    with pytest.raises(ValueError):
        mis_error.find_optimal_parameters()
    with pytest.raises(ValueError):
        mis_error.expected_energy([0, 1, 0, 1])

def test_add_nodes_and_edges():
    """Test adding nodes and edges to the graph."""
    mis.addNodes(4)
    assert mis.graph.num_nodes() == 4
    mis.addEdges([(0, 1), (1, 2), (2, 3), (3, 0)])
    assert mis.graph.num_edges() == 4

def test_brute_force_solution():
    """Test the brute-force solution to the maximum independent set problem."""
    mis.buildQUBO()
    with patch.object(plt, "show"):
        mis.mis_brute_force(show_graph=True, print_expected_energy_bar=True)

def test_qaoa_solution():
    mis.buildCostHamiltonian()
    with patch.object(plt, "show"):
        mis.buildQAOAAnsatz(layers=2, draw_circuit=True)

    beta, gamma = mis.find_optimal_parameters()
    with patch.object(plt, "show"):
        mis.qaoa_evaluate(beta, gamma, 2 ** 16, print_count=True)

def test_misc():
    with patch.object(plt, "show"):
        mis.visualize()
