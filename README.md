# Evaluating Mobility Costs for Large Internet Topologies
Code to simulate multiple future internet architectures using a subset of the internet topology, and evaluate forwarding costs and update costs associated with mobility.

## Dataset
Dataset has been obtained from CAIDA, and contains inferred AS relationships for all internet ASes.
Inferred information is converted to a graphical structure, the results are parsed, pickled and stored.

## How to Run
1. `python generate_graph.py` generates the subset of the internet topology and creates the graph for future experiments.
2. `python ../Experiments/source_dest.py` generates different source and destination locations to simulate mobility.
3. Each experiment generates forwarding costs, and update costs for the chosen mobility locations.

## Dependencies
`pickle`,  `networkx`
