#!/bin/bash

for notebook in edgeless_graph.ipynb complete_graph.ipynb circular_graph.ipynb line_graph.ipynb random_graph.ipynb; do
    echo "Running $notebook"
    time jupyter nbconvert --execute --to pdf "$notebook"
done