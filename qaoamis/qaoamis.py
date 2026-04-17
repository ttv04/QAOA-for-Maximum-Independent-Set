"""Provide the primary functions."""
import numpy as np
import rustworkx as rx
from rustworkx.visualization import mpl_draw
import matplotlib.pyplot as plt
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.visualization import plot_histogram
from matplotlib.patches import Patch
from scipy.optimize import minimize

default_color = "#1f78b4"
mark_color = "red"
highest_energy_color = "orange"

class QAOAMIS:
    """The primary class for qaoamis."""
    def __init__(self):
        """Initialize the class."""
        self.graph = rx.PyGraph()
        self.n = 0
        self.Q = None
        self.H_C = None
        self.QAOAAnsatz = None

    def addNodes(self, n):
        """Add n nodes to the graph."""
        self.n = n
        self.graph.add_nodes_from(range(n))

    def addEdges(self, edges):
        """Add edges to the graph."""
        for x1, x2 in edges:
            self.graph.add_edge(x1, x2, None)

    def visualize(self):
        """Visualize the graph."""
        print(self.graph.num_nodes())
        mpl_draw(self.graph, with_labels=True, label=list(range(self.n)))

    def expected_energy(self, configuration):
        '''Calculate the expected energy of a given configuration.'''
        if self.Q is None:
            raise ValueError("QUBO matrix not built. Please call buildQUBO() before expected_energy().")
        
        return (configuration.T @ self.Q @ configuration).item()
    
    def mis_brute_force(self, show_graph=False, print_expected_energy_bar=False):
        '''Brute-force solution to the maximum independent set problem.'''

        # Default QUBO matrix if not built
        if self.Q is None:
            raise ValueError("QUBO matrix not built. Please call buildQUBO() before mis_brute_force().")

        map = dict()

        min_val = 0
        configuration = None
        for i in range(2**self.n):
            x = np.array([(i >> j) & 1 for j in range(self.n)])
            indep_set_value = x.T @ self.Q @ x
            if indep_set_value < min_val:
                min_val = indep_set_value
                configuration = x
            
            if print_expected_energy_bar:
                map[f"{i:0{self.n}b}"] = self.expected_energy(x)

        if show_graph:
            G = self.graph.copy()
            color = [mark_color if configuration[i] == 1 else default_color for i in range(self.n)]
            mpl_draw(G, with_labels=True, label=list(range(self.n)), node_color = color)

        if print_expected_energy_bar:

            highest_energy = max(map.values())
            for key in map.keys():
                map[key] = -map[key] + highest_energy

            x = list(map.keys())
            y = list(map.values())

            self._plot_with_all_xticks(x, y, 'Configuration (as integer)', 'Energy (inverted)', 'Expected Energy Landscape of the QUBO for Maximum Independent Set', hightlight_sol=True)
        
        return configuration
    
    def buildQUBO(self, penalty=None):
        '''Build the QUBO matrix for the maximum independent set problem.'''

        if self.graph.num_nodes() == 0:
            raise ValueError("Graph has no nodes. Please add at least a node before building QUBO.")

        if penalty is None:
            penalty = self.n

        Q = np.zeros((self.n, self.n))

        for i in range(self.n):
            Q[i, i] = -1

        for i, j in self.graph.edge_list():
            Q[i, j] = Q[j, i] = penalty / 2
        
        self.Q = Q
        return Q
    
    def buildCostHamiltonian(self, penalty=None):
        '''Build the cost Hamiltonian for the maximum independent set problem.'''
        
        if self.graph.num_nodes() == 0:
            raise ValueError("Graph has no nodes. Please add at least a node before building the cost Hamiltonian.")

        if penalty is None:
            penalty = self.n

        q = [-1] * self.n
        pauli_list = []

        # ZZ terms (edge penalties)
        for i, j in self.graph.edge_list():
            pauli_list.append(("ZZ", [i, j], penalty / 4))
            pauli_list.append(("Z", [i], -penalty / 4))
            pauli_list.append(("Z", [j], -penalty / 4))

        # Z terms (vertex rewards + edge corrections)
        for v in self.graph.node_indices():
            pauli_list.append(("Z", [v], -0.5 * q[v]))

        self.H_C = SparsePauliOp.from_sparse_list(pauli_list, self.n)

    def buildQAOAAnsatz(self, layers: int = 1, draw_circuit=False):
        if self.H_C is None:
            raise ValueError("Cost Hamiltonian not built. Please call buildCostHamiltonian() before buildQAOAAnsatz().")
        self.QAOAAnsatz = QAOAAnsatz(cost_operator=self.H_C, reps=layers)

        if draw_circuit:
            self.QAOAAnsatz.draw(output="mpl", interactive=True)

        return self.QAOAAnsatz

    # Might need to have a parameter determine the algorithm to find optimal parameters, e.g. COBYLA, SPSA, etc.
    def find_optimal_parameters(self) -> tuple[list[float], list[float]]:
        '''Find the optimal parameters for the QAOA circuit. Currently uses COBYLA optimization algorithm and initializes all gamma to pi and all beta to pi/2. Returns a tuple of two lists: the first list contains the optimal gamma values and the second list contains the optimal beta values.'''
        if self.QAOAAnsatz is None:
            raise ValueError("QAOA Ansatz not built. Please call buildQAOAAnsatz() before find_optimal_parameters().")
        
        init_gamma = [np.pi] * (self.QAOAAnsatz.reps)
        init_beta = [np.pi / 2] * (self.QAOAAnsatz.reps)

        result = minimize(self._objective, x0=init_beta + init_gamma, method='COBYLA')
        return (result.x[:self.QAOAAnsatz.reps], result.x[self.QAOAAnsatz.reps:])

    def qaoa_evaluate(self, beta: list[float], gamma: list[float], shots = 1024, print_count=False):
        '''Evaluate the QAOA simulation circuit for the given parameters.'''
        if self.QAOAAnsatz is None:
            raise ValueError("QAOA Ansatz not built. Please call buildQAOAAnsatz() before qaoa_evaluate().")

        params = list(beta) + list(gamma)
        param_dict = {self.QAOAAnsatz.parameters[i].name: params[i] for i in range(len(self.QAOAAnsatz.parameters))}
        circuit_bound = self.QAOAAnsatz.assign_parameters(param_dict)
        psi = Statevector(circuit_bound)

        result = psi.sample_counts(shots)

        if print_count:
            x = [f"{i:0{self.n}b}" for i in range(2**self.n)]
            y = [result.get(f"{i:0{self.n}b}", 0) for i in range(2**self.n)]
            self._plot_with_all_xticks(x, y, 'Configuration (as bitstring)', 'Counts', 'Measurement Results of the QAOA Circuit', hightlight_sol=False)
        
        return result


    def _objective(self, params):
        if self.QAOAAnsatz is None:
            raise ValueError("QAOA Ansatz not built. Please call buildQAOAAnsatz()")
        param_dict = {self.QAOAAnsatz.parameters[i].name: params[i] for i in range(len(self.QAOAAnsatz.parameters))}
        circuit_bound = self.QAOAAnsatz.assign_parameters(param_dict)
        psi = Statevector(circuit_bound)
        return np.real(psi.expectation_value(self.H_C))

    def _plot_with_all_xticks(self, x, y, x_label, y_label, title, hightlight_sol=False, space_per_tick=0.2):

        max_val = max(y)

        colors = [default_color] * len(x)

        if hightlight_sol:
            colors = [highest_energy_color if val == max_val else default_color for val in y]

        plt.figure(figsize=(12, 6))  # keep normal size
        plt.bar(x, y, color=colors)

        # Show all ticks, but make them compact
        plt.xticks(x, rotation=85, fontsize=6)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        plt.margins(x=0.01)   # reduce side padding
        plt.tight_layout()

        if hightlight_sol:
            legend_elements = [
                Patch(facecolor=default_color, label="Candidates"),
                Patch(facecolor=highest_energy_color, label=f"Solutions")
            ]
        else:
            legend_elements = [
                Patch(facecolor=default_color, label="Candidates")
            ]
        plt.legend(handles=legend_elements)

        plt.show()

    
