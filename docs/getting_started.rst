Getting Started
===============

Welcome to **qaoamis** 🎯

*qaoamis* is a Python package designed to experimentally solve the 
**Maximum Independent Set (MIS)** problem using quantum-inspired techniques 
and run scalable experiments.

----

.. note::
   This package is intended for research and experimentation with QAOA-style workflows.

----

Overview
--------

qaoamis integrates several scientific and quantum computing tools:

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - 🧮 NumPy, SciPy
     - Efficient numerical computation
   * - 📊 Matplotlib
     - Visualization of experiment results
   * - ⚛️ Qiskit
     - Quantum circuit simulation and execution
   * - 🕸️ RustworkX
     - Fast graph algorithms for MIS problems

----

.. rubric:: 📦 Dependencies

Make sure your environment includes:

.. code-block:: bash

   Python >= 3.11
   numpy
   matplotlib
   rustworkx
   qiskit
   scipy

----

Installation
------------

Clone the repository and install in editable mode:

.. code-block:: bash

   pip install -e .

----

.. tip::
   Using a virtual environment (``conda``) is highly recommended.

----

Next Steps
----------

- Explore experiment configurations
- Try different graph inputs
- Analyze output visualizations

.. important::
   Ensure all dependencies are correctly installed before running experiments.
